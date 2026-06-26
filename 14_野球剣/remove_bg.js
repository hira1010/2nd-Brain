const { GifUtil } = require('gifwrap');

async function processGif() {
    console.log("Reading GIF...");
    const gif = await GifUtil.read('anime_sway.gif');
    
    console.log("Processing frames...");
    for (const frame of gif.frames) {
        const data = frame.bitmap.data;
        // Make black pixels (or very dark) transparent
        for (let i = 0; i < data.length; i += 4) {
            const r = data[i];
            const g = data[i+1];
            const b = data[i+2];
            
            // Tolerance for black background.
            if (r < 15 && g < 15 && b < 15) {
                data[i+3] = 0; // Alpha 0
            }
        }
    }
    
    console.log("Writing GIF...");
    // Write out the modified frames
    await GifUtil.write('anime_sway_trans.gif', gif.frames, gif);
    console.log("Done!");
}

processGif().catch(console.error);
