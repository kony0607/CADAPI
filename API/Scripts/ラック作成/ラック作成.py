import adsk.core, adsk.fusion, math, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent

        # --- 1. 入力画面 ---
        (pitch_str, cancelled) = ui.inputBox('歯のピッチ (mm)', 'ラック設計', '12.38')
        if cancelled: return
        pitch = float(pitch_str)

        (num_teeth_str, cancelled) = ui.inputBox('歯数', 'ラック設計', '10')
        if cancelled: return
        num_teeth = int(num_teeth_str)

        # --- 2. 寸法設定 (cm単位) ---
        p_cm = pitch / 10.0
        tooth_h = 0.4  # 歯の高さ 4mm
        base_h = 0.5   # 土台の厚み 5mm
        rack_thickness = 0.8 # ラック自体の厚み（奥行き） 8mm
        
        # 溝の幅（ピニオンの歯に合わせて調整）
        w_bottom = 1.0 / 10.0 # 10mm
        w_top = 0.88 / 10.0   # 8.8mm

        sketches = rootComp.sketches
        sketch = sketches.add(rootComp.xYConstructionPlane)
        lines = sketch.sketchCurves.sketchLines

        # --- 3. 連続した一筆書きで外枠を描く ---
        # 開始点（左下）
        last_pt = adsk.core.Point3D.create(0, 0, 0)
        
        # ギザギザの上面を描く
        for i in range(num_teeth):
            base_x = i * p_cm
            
            # 歯の谷と山を一筆書きでつなぐ
            p1 = adsk.core.Point3D.create(base_x, base_h, 0)
            p2 = adsk.core.Point3D.create(base_x + (p_cm - w_bottom)/2, base_h, 0)
            p3 = adsk.core.Point3D.create(base_x + (p_cm - w_top)/2, base_h + tooth_h, 0)
            p4 = adsk.core.Point3D.create(base_x + (p_cm + w_top)/2, base_h + tooth_h, 0)
            p5 = adsk.core.Point3D.create(base_x + (p_cm + w_bottom)/2, base_h, 0)
            p6 = adsk.core.Point3D.create(base_x + p_cm, base_h, 0)

            if i == 0:
                lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), p1)
            
            lines.addByTwoPoints(p1, p2)
            lines.addByTwoPoints(p2, p3)
            lines.addByTwoPoints(p3, p4)
            lines.addByTwoPoints(p4, p5)
            lines.addByTwoPoints(p5, p6)
            last_pt = p6

        # 外枠を閉じる（右端から下へ、左へ、上へ）
        p_end_bottom = adsk.core.Point3D.create(last_pt.x, 0, 0)
        p_start_bottom = adsk.core.Point3D.create(0, 0, 0)
        
        lines.addByTwoPoints(last_pt, p_end_bottom)
        lines.addByTwoPoints(p_end_bottom, p_start_bottom)
        lines.addByTwoPoints(p_start_bottom, adsk.core.Point3D.create(0, base_h, 0))

        # --- 4. 押し出し（実体化） ---
        # 描いたスケッチの中から「閉じられた面」を探す
        prof = sketch.profiles.item(0)
        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        # 厚み分押し出す
        distance = adsk.core.ValueInput.createByReal(rack_thickness)
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)

        ui.messageBox(f'ラックのボディを作成しました！\n全長: {pitch * num_teeth} mm')

    except:
        if ui: ui.messageBox('失敗:\n{}'.format(traceback.format_exc()))