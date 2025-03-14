document.addEventListener("DOMContentLoaded", function () {
    const piano = document.querySelector(".hover"); 
    const hoverTexts = document.querySelectorAll(".hover-text");

    // listen for when the mouse hovers over the keyboard 
    piano.addEventListener("mouseover", function () {
        hoverTexts.forEach((text) => {
            text.style.opacity = "1";
        });
    });

    piano.addEventListener("mouseout", function () {
        hoverTexts.forEach((text) => {
            text.style.opacity = "0";
        });
    });

    // sound map 
    const sound = {65:"http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
                87:"http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
                83:"http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
                69:"http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
                68:"http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
                70:"http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
                84:"http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
                71:"http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
                89:"http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
                72:"http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
                85:"http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
                74:"http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
                75:"http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
                79:"http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
                76:"http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
                80:"http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
                186:"http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"};


    // letters associated with keys 
    const letterMap = {"A": 0, "S": 1, "D": 2, "F":3, "G":4, "H":5, "J":6,
        "K": 7, "L":8, ";":9,
        "W": 0, "E": 1,
        "T":0, "Y":1, "U":2,
        "O":0,"P":1};

    const whiteKeys = document.querySelectorAll(".whiteKeys > div");
    const blackKeys = document.querySelectorAll(".blackKeys > div");
    const blackKeys2 = document.querySelectorAll(".blackKeys2 > div");
    const blackKeys3 = document.querySelectorAll(".blackKeys3 > div");

    // whether the great one has been awoken 
    let awoken = false; 

    // container to hold letters typed 
    const typedLetters = [];

    // when a key is pressed down 
    function keyDown(event) {
        const keyPressed = event.key.toUpperCase();     // letter of the key
        const keyCode = event.keyCode;                  // key code of the letter  
        // check if the key is one in the keyboard on the screen 
        if (letterMap[keyPressed] !== undefined) {
            let index = letterMap[keyPressed];
            let key; 

            const white = ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"];
            const black = ["W", "E"];
            const black2 = ["T", "Y", "U"];
            // figure out which key on the piano is being played 
            if (white.indexOf(keyPressed) !== -1) {
                key = whiteKeys[index];
            } else if (black.indexOf(keyPressed) !== -1) {
                key = blackKeys[index];
            } else if (black2.indexOf(keyPressed) !== -1) {
                key = blackKeys2[index];
            } else {
                key = blackKeys3[index];
            }

            if(key) {
                // watch for sequence of letters pressed 
                if (keyPressed === "W") {
                    // if W is pressed, start letters sequence over 
                    typedLetters.length = 0;
                    typedLetters.push(keyPressed); 
                } else {
                    typedLetters.push(keyPressed); 
                }
                if (typedLetters.length === 8) {
                    // check if weseeyou has been typed 
                    const correctLetters = ["W", "E", "S", "E", "E", "Y", "O", "U"];
                    for (let i = 0; i < 8; i++) {
                        if (typedLetters[i] !== correctLetters[i]) {
                            typedLetters.length = 0; 
                            break; 
                        }
                    }
                }

                if (!awoken) {
                    // change the background color of the key when pressed 
                    key.style.backgroundColor = "#FB8C00";
                    // play key sound 
                    const audio = new Audio(sound[keyCode]);
                    audio.play();
                    
                    if (typedLetters.length === 8) {
                        awoken = true; 
                        // play creepy audio 
                        const creepyAudio = new Audio("https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1");
                        creepyAudio.play();
                    }
                    
                    console.log(typedLetters);
                } 

                if (awoken) {
                    // the great one has awoken 
                    document.querySelector('.greatOne').classList.add('visible');
                    document.querySelector('.greatOneText').classList.add('visible');
                    document.querySelector('.whiteKeys').classList.add('visible');
                    document.querySelector('.blackKeys').classList.add('visible');
                    document.querySelector('.blackKeys2').classList.add('visible');
                    document.querySelector('.blackKeys3').classList.add('visible');
                }
            }
        } 
    }

    function keyUp(event) {
        const keyPressed = event.key.toUpperCase();
        if (letterMap[keyPressed] !== undefined) {
            let index = letterMap[keyPressed];
            let key; 

            const white = ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"];
            const black = ["W", "E"];
            const black2 = ["T", "Y", "U"];
            // figure out which key needs to be reset 
            if (white.indexOf(keyPressed) !== -1) {
                key = whiteKeys[index];
            } else if (black.indexOf(keyPressed) !== -1) {
                key = blackKeys[index];
            } else if (black2.indexOf(keyPressed) !== -1) {
                key = blackKeys2[index];
            } else {
                key = blackKeys3[index];
            }

            if(key) {
                // set the key back to normal color 
                key.style.backgroundColor = "";
            }
        } 
    }
   

    // create listeners 
    document.addEventListener("keydown", keyDown);
    document.addEventListener("keyup", keyUp);
});
