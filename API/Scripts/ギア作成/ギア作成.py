import adsk.core, adsk.fusion, math, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent

        # --- 設定寸法 (mm単位) ---
        d_outer = 35.0       # 外径
        d_inner = 28.043     # 歯底径
        d_hole  = 3.4        # 中心軸穴
        thickness = 8.0      # ギアの厚み
        num_teeth = 8        # 歯数
        
        w_tip  = 8.6314      # 外側（歯先）の幅：狭く
        w_root = 9.672       # 内側（根元）の幅：広く
        
        # 【修正箇所】M2ネジ用の穴径
        d_screw = 2.4        

        # --- 計算処理 (cm変換) ---
        r_outer = d_outer / 20.0
        r_inner = d_inner / 20.0
        r_hole  = d_hole / 20.0
        h = thickness / 10.0

        angle_tip  = (w_tip / (d_outer / 2.0)) / 2.0
        angle_root = (w_root / (d_inner / 2.0)) / 2.0
        angle_step = (2 * math.pi) / num_teeth
        rotate_offset = angle_step / 2.0

        # --- 1. ギア本体の作成 ---
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

        # --- 2. 側面のネジ穴作成 (2.4mm) ---
        sketch2 = sketches.add(rootComp.xZConstructionPlane)
        # 穴の中心を厚みの半分(4mm)に配置
        screw_center = adsk.core.Point3D.create(r_outer, h / 2.0, 0)
        sketch2.sketchCurves.sketchCircles.addByCenterRadius(screw_center, d_screw / 20.0)
        
        prof2 = sketch2.profiles.item(0)
        cutInput = extrudes.createInput(prof2, adsk.fusion.FeatureOperations.CutFeatureOperation)
        dist = adsk.core.ValueInput.createByReal(-r_outer)
        cutInput.setDistanceExtent(False, dist)
        cutInput.participantBodies = [targetBody]
        extrudes.add(cutInput)

        ui.messageBox(f'M2ネジ用(穴径{d_screw}mm)のギアが完成しました！')

    except:
        if ui: ui.messageBox('失敗:\n{}'.format(traceback.format_exc()))