Separated rig asset layout for Airi

Place transparent 640x640 PNG files in:
images/parts/<pose>/

Required:
- legs.png
- torso.png
- head.png

Optional:
- eyes.png
- mouth.png
- hair_front.png
- fx_front.png

Rules:
- Keep every part on the same 640x640 canvas.
- Do not crop tightly. Use transparency around the part.
- Align all parts to the original full-body pose.
- The game uses the rig automatically when all required files exist.
- If parts are missing, it falls back to the current single-image display.
