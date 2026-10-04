// ================================================
// API URL
// ================================================

const API_URL = "http://127.0.0.1:8000";


// ================================================
// Generate Lyrics
// ================================================

async function generateLyrics() {

    const songName =
        document.getElementById("songName").value.trim();

    const genre =
        document.getElementById("genre").value;

    const mood =
        document.getElementById("mood").value;

    const language =
        document.getElementById("language").value;

    const verses =
        Number(
            document.getElementById("verses").value
        );


    // --------------------------------------------
    // Validate song name
    // --------------------------------------------

    if (!songName) {

        showError(
            "Please enter a song name or topic."
        );

        return;

    }


    // --------------------------------------------
    // Validate verses
    // --------------------------------------------

    if (verses < 1 || verses > 8) {

        showError(
            "Number of verses must be between 1 and 8."
        );

        return;

    }


    // --------------------------------------------
    // UI - Loading
    // --------------------------------------------

    setLoading(true);

    hideError();

    document.getElementById("result").style.display =
        "none";


    try {

        console.log("Sending request:", {
            song_name: songName,
            genre: genre,
            mood: mood,
            language: language,
            verses: verses
        });


        // ----------------------------------------
        // Send request to FastAPI
        // ----------------------------------------

        const response = await fetch(
            `${API_URL}/generate`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    song_name: songName,

                    genre: genre,

                    mood: mood,

                    language: language,

                    verses: verses

                })
            }
        );


        // ----------------------------------------
        // Read response
        // ----------------------------------------

        const data =
            await response.json();


        console.log(
            "API response:",
            data
        );


        // ----------------------------------------
        // Handle API error
        // ----------------------------------------

        if (!response.ok) {

            throw new Error(
                data.error ||
                "Server returned an error."
            );

        }


        if (data.error) {

            throw new Error(
                data.error
            );

        }


        // ----------------------------------------
        // Display lyrics
        // ----------------------------------------

        document.getElementById(
            "resultTitle"
        ).textContent =
            data.song_name;


        document.getElementById(
            "lyrics"
        ).textContent =
            data.lyrics;


        document.getElementById(
            "result"
        ).style.display =
            "block";


        // Scroll to result

        document.getElementById(
            "result"
        ).scrollIntoView({
            behavior: "smooth",
            block: "start"
        });


    }


    catch (error) {

        console.error(
            "Generation error:",
            error
        );


        showError(
            error.message ||
            "Could not connect to the AI server."
        );

    }


    finally {

        setLoading(false);

    }

}


// ================================================
// Loading State
// ================================================

function setLoading(isLoading) {

    const button =
        document.getElementById(
            "generateButton"
        );

    const buttonText =
        document.getElementById(
            "buttonText"
        );

    const buttonLoader =
        document.getElementById(
            "buttonLoader"
        );

    const loading =
        document.getElementById(
            "loading"
        );


    if (isLoading) {

        button.disabled = true;

        buttonText.style.display =
            "none";

        buttonLoader.style.display =
            "inline";

        loading.style.display =
            "block";

    }

    else {

        button.disabled = false;

        buttonText.style.display =
            "inline";

        buttonLoader.style.display =
            "none";

        loading.style.display =
            "none";

    }

}


// ================================================
// Copy Lyrics
// ================================================

async function copyLyrics() {

    const lyrics =
        document.getElementById(
            "lyrics"
        ).textContent;


    if (!lyrics) {

        return;

    }


    try {

        await navigator.clipboard.writeText(
            lyrics
        );

        alert(
            "Lyrics copied to clipboard! 🎵"
        );

    }

    catch (error) {

        console.error(error);

        alert(
            "Could not copy lyrics."
        );

    }

}


// ================================================
// Download Lyrics
// ================================================

function downloadLyrics() {

    const lyrics =
        document.getElementById(
            "lyrics"
        ).textContent;


    const songName =
        document.getElementById(
            "resultTitle"
        ).textContent;


    if (!lyrics) {

        return;

    }


    const fileContent =
        `${songName}\n\n${lyrics}`;


    const blob =
        new Blob(
            [fileContent],
            {
                type: "text/plain;charset=utf-8"
            }
        );


    const url =
        URL.createObjectURL(blob);


    const link =
        document.createElement("a");


    link.href = url;

    link.download =
        `${songName || "generated-lyrics"}.txt`;


    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);


    URL.revokeObjectURL(url);

}


// ================================================
// Error Handling
// ================================================

function showError(message) {

    const error =
        document.getElementById(
            "error"
        );


    error.textContent =
        `⚠️ ${message}`;


    error.style.display =
        "block";


    error.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });

}


function hideError() {

    const error =
        document.getElementById(
            "error"
        );


    error.style.display =
        "none";

}


// ================================================
// Enter Key Support
// ================================================

document.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            event.ctrlKey
        ) {

            generateLyrics();

        }

    }
);
