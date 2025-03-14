// feedback button 
const feedbackbutton = document.getElementById("feedbackbutton");
const form = document.getElementById("feedbackform");
// when the feedback button is pressed, have the form appear 
feedbackbutton.addEventListener("click", () => {
    form.style.display = form.style.display === 'none' || form.style.display === '' ? 'block' : 'none';
});
