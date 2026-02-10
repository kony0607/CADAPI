import adsk.core, adsk.fusion, math, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        if not design:
            ui.messageBox('ドキュメントが開かれていません。')
            return
        rootComp = design.rootComponent

        # --- 1. 入力画面（ダイアログ）を表示 ---
        # 外径
        (d_outer_str, cancelled) = ui.inputBox('外径を入力 (mm)', 'ピニオン設計', '35.0')
        if cancelled: return
        d_outer = float(d_outer_str)

        # 歯底径
        (d_inner_str, cancelled) = ui.inputBox('歯底径を入力 (mm)', 'ピニオン設計', '28.043')
        if cancelled: return
        d_inner = float(d_inner_str)

        # 歯数
        (num_teeth_str, cancelled) = ui.inputBox('歯数を入力 (枚)', 'ピニオン設計', '8')
        if cancelled: return
        num_teeth = int(num_teeth_str)

        # 厚み
        (thickness_str, cancelled) = ui.inputBox('ギアの厚みを入力 (mm)', 'ピニオン設計', '8.0')
        if cancelled: return
        thickness = float(thickness_str)

        # 固定ネジ穴
        (d_screw_str, cancelled) = ui.inputBox('ネジ穴径を入力 (mm)', 'ピニオン設計', '2.4')
        if cancelled: return
        d_screw = float(d_screw_str)

        # --- 2. 固定値の計算 (cm変換) ---
        d_hole = 3.4  # 中心軸穴
        w_tip = 8.6314
        w_root = 9.672
       
        r_outer = d_outer / 20.0
        r_inner = d_inner / 20.0
        r_hole  = d_hole / 20.0
        h = thickness / 10.0

        angle_tip  = (w_tip / (d_outer / 2.0)) / 2.0
        angle_root = (w_root / (d_inner / 2.0)) / 2.0
        angle_step = (2 * math.pi) / num_teeth
        rotate_offset = angle_step / 2.0

        # --- 3. ギア本体の作成 ---
        sketches = rootComp.sketches
        sketch1 = sketches.add(rootComp.xYConstructionPlane)
        lines = sketch1.sketchCurves.sketchLines
        arcs = sketch1.sketchCurves.sketchArcs
        center_pt = adsk.core.Point3D.create(0, 0, 0)

        for i in range(num_teeth):
            offset = i * angle_step + rotate_offset
            p1 = adsk.core.Point3D.create(r_outer * math.cos(offset - angle_tip), r_outer * math.sin(offset - angle_tip), 0)
            p2 = adsk.core.Point3D.create(r_outer * math.cos(offset + angle_tip), r_outer * math.sin(offset + angle_tip), 0)
            p3 = adsk.core.Point3D.create(r_inner * math.cos(offset + angle_root), r_inner * math.sin(offset + angle_root), 0)
            p4 = adsk.core.Point3D.create(r_inner * math.cos(offset - angle_root), r_inner * math.sin(offset - angle_root), 0)
           
            lines.addByTwoPoints(p2, p3)
            lines.addByTwoPoints(p4, p1)
            arcs.addByCenterStartEnd(center_pt, p1, p2)
           
            next_offset = (i + 1) * angle_step + rotate_offset
            p_next = adsk.core.Point3D.create(r_inner * math.cos(next_offset - angle_root), r_inner * math.sin(next_offset - angle_root), 0)
            arcs.addByCenterStartEnd(center_pt, p3, p_next)

        sketch1.sketchCurves.sketchCircles.addByCenterRadius(center_pt, r_hole)
       
        prof = sketch1.profiles.item(0)
        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(h))
        gearFeature = extrudes.add(extInput)
        targetBody = gearFeature.bodies.item(0)

        # --- 4. 側面のネジ穴作成 ---
        sketch2 = sketches.add(rootComp.xZConstructionPlane)
        screw_center = adsk.core.Point3D.create(r_outer, h / 2.0, 0)
        sketch2.sketchCurves.sketchCircles.addByCenterRadius(screw_center, d_screw / 20.0)
       
        prof2 = sketch2.profiles.item(0)
        cutInput = extrudes.createInput(prof2, adsk.fusion.FeatureOperations.CutFeatureOperation)
        dist = adsk.core.ValueInput.createByReal(-r_outer)
        cutInput.setDistanceExtent(False, dist)
        cutInput.participantBodies = [targetBody]
        extrudes.add(cutInput)

        ui.messageBox(f'設計完了！\n外径:{d_outer}mm, 歯数:{num_teeth}枚\n厚み:{thickness}mm')

    except:
        if ui: ui.messageBox('失敗:\n{}'.format(traceback.format_exc()))
