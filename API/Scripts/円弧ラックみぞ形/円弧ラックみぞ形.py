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
        # 【設定シート：シンプル分割版】
        # ==========================================================
        R_RACK       = 800.0   # 半径
        PITCH        = 12.38   # ピッチ
        START_DEGREE = 30.0    # 開始角度
        END_DEGREE   = 80.0    # 終了角度
        DIVISIONS    = 6       # 3分割
        
        HOLE_W       = 10.513  # 窓幅
        RACK_H       = 30.0    # 全高 (アルミ板50mm幅用)
        GEAR_WINDOW_H = 9.6   # 窓（穴）の高さ
        RACK_T       = 8.0     # ラック自体の厚み (設計図の8mm)
        
        # 溝（スリット）設定
        SLIT_WIDTH   = 3.6     
        SLIT_DEPTH   = 4.0     
        # ==========================================================

        R, P = R_RACK/10.0, PITCH/10.0
        HW = HOLE_W/10.0
        RH, GH = RACK_H/10.0, GEAR_WINDOW_H/10.0
        T = RACK_T / 10.0
        SW, SD = SLIT_WIDTH/10.0, SLIT_DEPTH/10.0
        
        angle_step = P / R
        pillar_ang = angle_step - (HW / R)
        
        total_span_rad = math.radians(END_DEGREE - START_DEGREE)
        total_holes = int(total_span_rad / angle_step)
        holes_per_part = total_holes // DIVISIONS
        
        sketches = rootComp.sketches
        extrudes = rootComp.features.extrudeFeatures
        xyPlane = rootComp.xYConstructionPlane
        center_pt = adsk.core.Point3D.create(0, 0, 0)

        for p_idx in range(DIVISIONS):
            current_start_ang = math.radians(START_DEGREE) + (p_idx * holes_per_part * angle_step)
            current_num_holes = holes_per_part if p_idx < DIVISIONS - 1 else total_holes - (holes_per_part * (DIVISIONS - 1))
            part_span = (angle_step * current_num_holes) + pillar_ang

            # 1. パーツ本体（円弧状の板）を作成
            sketch_base = sketches.add(xyPlane)
            r_out, r_in = R + T/2, R - T/2
            
            arcs = []
            for rad in [r_out, r_in]:
                arcs.append(sketch_base.sketchCurves.sketchArcs.addByCenterStartEnd(center_pt,
                    adsk.core.Point3D.create(rad * math.cos(current_start_ang), rad * math.sin(current_start_ang), 0),
                    adsk.core.Point3D.create(rad * math.cos(current_start_ang + part_span), rad * math.sin(current_start_ang + part_span), 0)))
            sketch_base.sketchCurves.sketchLines.addByTwoPoints(arcs[0].startSketchPoint, arcs[1].startSketchPoint)
            sketch_base.sketchCurves.sketchLines.addByTwoPoints(arcs[0].endSketchPoint, arcs[1].endSketchPoint)
            
            prof_base = sketch_base.profiles.item(0)
            ext_base = extrudes.addSimple(prof_base, adsk.core.ValueInput.createByReal(RH), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            body = ext_base.bodies.item(0)
            body.name = f"SimpleRack_Part_{p_idx + 1}"

            # 2. 窓をくり抜く
            rail_h = (RH - GH) / 2.0
            for i in range(current_num_holes):
                ang_c = current_start_ang + (i * angle_step) + pillar_ang + (HW/R)/2
                ang_s, ang_e = ang_c - (HW/R)/2, ang_c + (HW/R)/2
                
                sketch_cut = sketches.add(xyPlane)
                pts = [
                    adsk.core.Point3D.create((r_in-0.1)*math.cos(ang_s), (r_in-0.1)*math.sin(ang_s), 0),
                    adsk.core.Point3D.create((r_out+0.1)*math.cos(ang_s), (r_out+0.1)*math.sin(ang_s), 0),
                    adsk.core.Point3D.create((r_out+0.1)*math.cos(ang_e), (r_out+0.1)*math.sin(ang_e), 0),
                    adsk.core.Point3D.create((r_in-0.1)*math.cos(ang_e), (r_in-0.1)*math.sin(ang_e), 0)
                ]
                for j in range(4): sketch_cut.sketchCurves.sketchLines.addByTwoPoints(pts[j], pts[(j+1)%4])
                
                ext_h = extrudes.createInput(sketch_cut.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
                ext_h.startExtent = adsk.fusion.OffsetStartDefinition.create(adsk.core.ValueInput.createByReal(rail_h))
                ext_h.setDistanceExtent(False, adsk.core.ValueInput.createByReal(GH))
                ext_h.participantBodies = [body]
                extrudes.add(ext_h)

            # 3. 背面にアルミ板用の溝（スリット）を彫る
            sketch_slit = sketches.add(xyPlane)
            r_s_in, r_s_out = r_in - 0.1, r_in + SD # 内側から深さSD分彫り込む
            
            arcs_s = []
            for rad in [r_s_in, r_s_out + SW]: # 幅SW分
                # スリットの正確な位置：内側の壁(r_in)から深さSD分、幅SW分
                pass # ここは単純化して内面からのカットにします

            # ※スリットのロジックをより確実に（内側面に溝を作る）
            # ここではシンプルに内側の円弧からオフセットした領域をカット
            sketch_slit = sketches.add(xyPlane)
            # 内側の壁からSW(3.6mm)分の厚みを、SD(4mm)の深さで削り取る
            arc_s1 = sketch_slit.sketchCurves.sketchArcs.addByCenterStartEnd(center_pt,
                adsk.core.Point3D.create(r_in * math.cos(current_start_ang), r_in * math.sin(current_start_ang), 0),
                adsk.core.Point3D.create(r_in * math.cos(current_start_ang + part_span), r_in * math.sin(current_start_ang + part_span), 0))
            arc_s2 = sketch_slit.sketchCurves.sketchArcs.addByCenterStartEnd(center_pt,
                adsk.core.Point3D.create((r_in + SD) * math.cos(current_start_ang), (r_in + SD) * math.sin(current_start_ang), 0),
                adsk.core.Point3D.create((r_in + SD) * math.cos(current_start_ang + part_span), (r_in + SD) * math.sin(current_start_ang + part_span), 0))
            sketch_slit.sketchCurves.sketchLines.addByTwoPoints(arc_s1.startSketchPoint, arc_s2.startSketchPoint)
            sketch_slit.sketchCurves.sketchLines.addByTwoPoints(arc_s1.endSketchPoint, arc_s2.endSketchPoint)
            
            # 中央部分（窓の上下）にスリットを彫る
            ext_s = extrudes.createInput(sketch_slit.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
            ext_s.setDistanceExtent(False, adsk.core.ValueInput.createByReal(RH))
            ext_s.participantBodies = [body]
            # アルミ板の厚み分(SW)だけ浮かせてカットするか、全高カットするか
            # ここではシンプルに全高スリット（コの字断面）にします
            extrudes.add(ext_s)

        ui.messageBox('シンプル分割ラック完成！\n取り付け用ベースなしのハシゴ形状のみです。')
    except:
        if ui: ui.messageBox('失敗:\n{}'.format(traceback.format_exc()))