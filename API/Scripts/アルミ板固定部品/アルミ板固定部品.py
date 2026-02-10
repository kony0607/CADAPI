import adsk.core, adsk.fusion, math, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        if not design: return
        rootComp = design.rootComponent

        # ==========================================================
        # 【テスト印刷用 設定シート】
        # ==========================================================
        NUM_HOLES   = 10      # テスト用に10個だけ生成
        
        # 寸法パラメータ
        R_RACK      = 800.0   # 半径 800mm
        PITCH       = 12.38   # ピッチ
        HOLE_W      = 10.513  # 窓の幅（ギアの遊び含む）
        
        RACK_H      = 50.0    # 全高 (アルミ板50mmに合わせる)
        GEAR_WINDOW_H = 12.0  # ギアが通る窓の高さ
        
        RACK_T      = 10.0    # ラック部分の厚み
        BACK_T      = 5.0     # 背面フレーム固定部の厚み
        
        # 溝（スリット）設定
        SLIT_WIDTH  = 3.6     # アルミ板用溝 (3.5~3.6mm推奨)
        SLIT_DEPTH  = 8.0     # しっかり深く刺さるように深めに設定
        
        # ネジ穴
        SCREW_DIA   = 3.4     # M3用穴
        # ==========================================================

        # 単位変換 (mm -> cm)
        R, P = R_RACK/10.0, PITCH/10.0
        HW = HOLE_W/10.0
        RH, GH = RACK_H/10.0, GEAR_WINDOW_H/10.0
        T, BT = RACK_T/10.0, BACK_T/10.0
        SW, SD = SLIT_WIDTH/10.0, SLIT_DEPTH/10.0

        angle_step = P / R
        pillar_ang = angle_step - (HW / R)
        total_angle = (angle_step * NUM_HOLES) + pillar_ang

        sketches = rootComp.sketches
        extrudes = rootComp.features.extrudeFeatures
        xyPlane = rootComp.xYConstructionPlane
        center_pt = adsk.core.Point3D.create(0, 0, 0)

        # 1. 土台（ラック+背面）を大きなブロックとして作成
        sketch_base = sketches.add(xyPlane)
        r_outer = R + T/2
        r_inner = R - T/2 - BT # 背面プレートの裏側まで
        
        # 扇形を描画
        arcs = []
        for rad in [r_outer, r_inner]:
            arcs.append(sketch_base.sketchCurves.sketchArcs.addByCenterStartEnd(center_pt,
                adsk.core.Point3D.create(rad, 0, 0),
                adsk.core.Point3D.create(rad * math.cos(total_angle), rad * math.sin(total_angle), 0)))
        sketch_base.sketchCurves.sketchLines.addByTwoPoints(arcs[0].startSketchPoint, arcs[1].startSketchPoint)
        sketch_base.sketchCurves.sketchLines.addByTwoPoints(arcs[0].endSketchPoint, arcs[1].endSketchPoint)
        
        prof_base = sketch_base.profiles.item(0)
        ext_base = extrudes.createInput(prof_base, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        ext_base.setDistanceExtent(False, adsk.core.ValueInput.createByReal(RH))
        base_body = extrudes.add(ext_base).bodies.item(0)

        # 2. ギアの「窓」をくり抜く (Cut)
        # 上下のレールの残りを計算
        rail_h = (RH - GH) / 2.0
        
        # 窓を開ける領域のスケッチ
        for i in range(NUM_HOLES):
            ang_center = (i * angle_step) + pillar_ang + (HW/R)/2
            ang_start  = ang_center - (HW/R)/2
            ang_end    = ang_center + (HW/R)/2
            
            sketch_cut = sketches.add(xyPlane)
            # 窓はラック部分(R-T/2 ～ R+T/2)だけ開ける
            r_cut_in  = R - T/2 + 0.01 # ギリギリを攻めないよう微調整
            r_cut_out = R + T/2 + 0.1  # 確実に突き抜ける
            
            p1 = adsk.core.Point3D.create(r_cut_in * math.cos(ang_start), r_cut_in * math.sin(ang_start), 0)
            p2 = adsk.core.Point3D.create(r_cut_out * math.cos(ang_start), r_cut_out * math.sin(ang_start), 0)
            p3 = adsk.core.Point3D.create(r_cut_out * math.cos(ang_end), r_cut_out * math.sin(ang_end), 0)
            p4 = adsk.core.Point3D.create(r_cut_in * math.cos(ang_end), r_cut_in * math.sin(ang_end), 0)
            
            lines = sketch_cut.sketchCurves.sketchLines
            lines.addByTwoPoints(p1, p2); lines.addByTwoPoints(p2, p3)
            lines.addByTwoPoints(p3, p4); lines.addByTwoPoints(p4, p1)
            
            prof_cut = sketch_cut.profiles.item(0)
            ext_cut = extrudes.createInput(prof_cut, adsk.fusion.FeatureOperations.CutFeatureOperation)
            # 高さ方向の範囲指定（中心部分だけ抜く）
            start_offset = adsk.core.ValueInput.createByReal(rail_h)
            dist = adsk.core.ValueInput.createByReal(GH)
            ext_cut.startExtent = adsk.fusion.OffsetStartDefinition.create(start_offset)
            ext_cut.setDistanceExtent(False, dist)
            ext_cut.participantBodies = [base_body]
            extrudes.add(ext_cut)

        # 3. アルミ板用の溝を彫る (Cut)
        sketch_slit = sketches.add(xyPlane)
        r_slit_center = R - T/2 # ラックと背板の境界あたりに溝
        r_s_in  = r_slit_center - SW/2
        r_s_out = r_slit_center + SW/2
        
        arcs_s = []
        for rad in [r_s_in, r_s_out]:
            arcs_s.append(sketch_slit.sketchCurves.sketchArcs.addByCenterStartEnd(center_pt,
                adsk.core.Point3D.create(rad, 0, 0),
                adsk.core.Point3D.create(rad * math.cos(total_angle), rad * math.sin(total_angle), 0)))
        sketch_slit.sketchCurves.sketchLines.addByTwoPoints(arcs_s[0].startSketchPoint, arcs_s[1].startSketchPoint)
        sketch_slit.sketchCurves.sketchLines.addByTwoPoints(arcs_s[0].endSketchPoint, arcs_s[1].endSketchPoint)
        
        prof_slit = sketch_slit.profiles.item(0)
        ext_slit = extrudes.createInput(prof_slit, adsk.fusion.FeatureOperations.CutFeatureOperation)
        ext_slit.setDistanceExtent(False, adsk.core.ValueInput.createByReal(SD)) # 底から深さSDまで
        ext_slit.participantBodies = [base_body]
        extrudes.add(ext_slit)

        # 4. 固定用ネジ穴 (Cut)
        sketch_bolt = sketches.add(xyPlane)
        bolt_r = R - T/2 - BT/2.0 # 背板の中心
        
        # 両端と中央に穴
        for ang in [pillar_ang/2, total_angle/2, total_angle - pillar_ang/2]:
            cp = adsk.core.Point3D.create(bolt_r * math.cos(ang), bolt_r * math.sin(ang), 0)
            sketch_bolt.sketchCurves.sketchCircles.addByCenterRadius(cp, SCREW_DIA/20.0)
        
        if sketch_bolt.profiles.count > 0:
            coll = adsk.core.ObjectCollection.create()
            for p in sketch_bolt.profiles: coll.add(p)
            ext_bolt = extrudes.createInput(coll, adsk.fusion.FeatureOperations.CutFeatureOperation)
            ext_bolt.setDistanceExtent(False, adsk.core.ValueInput.createByReal(RH))
            ext_bolt.participantBodies = [base_body]
            extrudes.add(ext_bolt)

        ui.messageBox('テスト印刷用パーツ完成！\n1. 溝がちゃんとあるか確認\n2. STLで書き出し\n3. 印刷してアルミ板とギアをテストしてください')
    except:
        if ui: ui.messageBox('失敗:\n{}'.format(traceback.format_exc()))