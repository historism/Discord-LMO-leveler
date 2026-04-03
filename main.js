async function runGatheringLoop() {
    const GATHER_TIME = 50;  
    const MIN_REST    = 300; 
    const REST_RANGE  = 0;  

    const AUTH_TOKEN = ""; 
    const SUPER_PROPS = "";

    let currentXP = 0; 

    const commonHeaders = {
        "Authorization": AUTH_TOKEN,
        "X-Super-Properties": SUPER_PROPS,
        "X-Discord-Locale": "en-US",
        "X-Discord-Timezone": "Europe/Berlin",
        "X-Debug-Options": "bugReporterEnabled",
        "Content-Type": "application/json",
        "Accept": "*/*"
    };
    const startGathering = async () => {
        return fetch("https://discord.com/api/v9/gorilla/activity/gathering/start", {
            method: "POST",
            headers: commonHeaders,
            body: "" 
        });
    };

    const completeGathering = async (xpValue) => {
        const completionBody = {
            "user_data": {
                "user_id": "430772757643395074",
                "crafting_class": "armor_crafter",
                "combat_class": "dps",
                "has_started_gathering": false,
                "xp": xpValue + 100 
            }
        };

        const response = await fetch("https://discord.com/api/v9/gorilla/activity/gathering/complete", {
            method: "POST",
            headers: commonHeaders,
            body: JSON.stringify(completionBody)
        });

        if (response.ok) {
            const data = await response.json();
            return data.user_data.xp; 
        } else {
            const errorText = await response.text();
            throw new Error(`Complete failed (${response.status}): ${errorText}`);
        }
    };

    while (true) {
        try {
            console.log(`[START] XP: ${currentXP}`);
            
            const sRes = await startGathering();
            if (!sRes.ok) console.warn(`Start Request gave status: ${sRes.status}`);

            await new Promise(r => setTimeout(r, GATHER_TIME));

            console.log("[COMPLETE] Completing...");
            currentXP = await completeGathering(currentXP);
            
            console.log(`%c[COMPLETE] New XP: ${currentXP}`);

            const nextRun = Math.floor(Math.random() * REST_RANGE) + MIN_REST;
            console.log(`%c[IDLE] Sleeping for ${nextRun}ms...`);
            await new Promise(r => setTimeout(r, nextRun));
            
        } catch (err) {
            console.error("Critical Error in Loop:", err);
            console.log("Waiting 30s before trying to recover...");
            await new Promise(r => setTimeout(r, 30000));
        }
    }
}

runGatheringLoop();