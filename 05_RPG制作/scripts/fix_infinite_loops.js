const fs = require('fs');
const path = require('path');

function fixMapRisks(projectPath) {
    const dataPath = path.join(projectPath, 'data');
    const files = fs.readdirSync(dataPath);
    const mapFiles = files.filter(f => f.match(/^Map\d{3}\.json$/)).map(f => path.join(dataPath, f));
    
    let fixedCount = 0;
    
    mapFiles.forEach(mapFile => {
        let data;
        try {
            data = JSON.parse(fs.readFileSync(mapFile, 'utf8'));
        } catch (e) {
            return;
        }
        
        let modified = false;
        if (!data.events) return;
        
        data.events.forEach(event => {
            if (!event) return;
            
            event.pages.forEach(page => {
                // Current active tool flags Parallel (4) and Autorun (3) if NO Wait (230)
                if ([3, 4].includes(page.trigger)) {
                    const list = page.list;
                    if (!list || list.length === 0) return;
                    
                    const hasExplicitWait = list.some(c => c.code === 230);
                    
                    if (!hasExplicitWait) {
                        const waitCmd = { code: 230, indent: 0, parameters: [1] };
                        const lastCmd = list[list.length - 1];
                        if (lastCmd && lastCmd.code === 0) {
                            list.splice(list.length - 1, 0, waitCmd);
                        } else {
                            list.push(waitCmd);
                        }
                        
                        console.log(`Fixed loop risk in ${path.basename(mapFile)} Event ${event.id} (${event.name})`);
                        modified = true;
                        fixedCount++;
                    }
                }
            });
        });
        
        if (modified) {
            fs.writeFileSync(mapFile, JSON.stringify(data));
        }
    });
    
    return fixedCount;
}

const count = fixMapRisks('c:/Users/hirak/Desktop/2nd-Brain/05_RPG制作');
console.log(`Total fixes applied: ${count}`);
