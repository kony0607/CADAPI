import adsk.core, adsk.fusion, math, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        if not design: return
        rootComp = design.rootComponent

        # --- 15x15フレーム用 パラメータ (mm) ---
        F_SIZE = 15.0      # フレーム角
        T = 5.0            # 肉厚
        BRACKET_W = 25.0   # ブラケットの奥行き
        PLATE_W = 50.0     # アルミ板の幅
        SLIT_T = 3.2       # 板の隙間（3mm板用）
        
        # 単位変換 mm -> cm
        fs, t, bw = F_SIZE/10, T/10, BRACKET_W/10
        pw, st = PLATE_W/10, SLIT_T/10

        sketches = rootComp.sketches
        extrudes = rootComp.features.extrudeFeatures
        
        # 1. 断面スケッチ (YZ平面)
        yzPlane = rootComp.yZConstructionPlane
        sketch = sketches.add(yzPlane)
        lines = sketch.sketchCurves.sketchLines
        
        # フレーム(15mm)を抱え込み、板(50mm)を支えるL字形状
        p1 = adsk.core.Point3D.create(0, 0, 0)
        p2 = adsk.core.Point3D.create(fs, 0, 0)
        p3 = adsk.core.Point3D.create(fs, t, 0)
        p4 = adsk.core.Point3D.create(t, t, 0)
        p5 = adsk.core.Point3D.create(t, pw, 0) # 垂直壁
        p6 = adsk.core.Point3D.create(-st-t, pw, 0)
        p7 = adsk.core.Point3D.create(-st-t, 0, 0)
        p8 = adsk.core.Point3D.create(-st, 0, 0)
        p9 = adsk.core.Point3D.create(-st, -fs, 0)
        p10 = adsk.core.Point3D.create(0, -fs, 0)

        lines.addByTwoPoints(p1, p2); lines.addByTwoPoints(p2, p3)
        lines.addByTwoPoints(p3, p4); lines.addByTwoPoints(p4, p5)
        lines.addByTwoPoints(p5, p6); lines.addByTwoPoints(p6, p7)
        lines.addByTwoPoints(p7, p8); lines.addByTwoPoints(p8, p9)
        lines.addByTwoPoints(p9, p10); lines.addByTwoPoints(p10, p1)

        # 2. 押し出し
        prof = sketch.profiles.item(0)
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(bw))
        extrudes.add(extInput)

        # 3. 穴あけ (15mmフレームのセンター 7.5mmを狙う)
        
        # ① 上面固定穴 (垂直方向)
        xyPlane = rootComp.xYConstructionPlane
        sketch_top = sketches.add(xyPlane)
        sketch_top.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(fs/2, bw/2, 0), 0.275) # M5穴想定
        
        ext_top = extrudes.createInput(sketch_top.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
        ext_top.setDistanceExtent(False, adsk.core.ValueInput.createByReal(t*2))
        extrudes.add(ext_top)

        # ② 側面固定穴 (水平方向)
        xzPlane = rootComp.xZConstructionPlane
        sketch_side = sketches.add(xzPlane)
        sketch_side.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(fs/2, -bw/2, 0), 0.275)
        
        ext_side = extrudes.createInput(sketch_side.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
        ext_side.setDistanceExtent(False, adsk.core.ValueInput.createByReal(t*2))
        extrudes.add(ext_side)

        ui.messageBox('15mmフレーム用ブラケット生成完了！\n上面・側面の中心に穴を配置しました。')
    except:
        if ui: ui.messageBox('失敗:\n{}'.format(traceback.format_exc()))