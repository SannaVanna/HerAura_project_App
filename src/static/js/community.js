
function toggleComments(postId){
    alert("Button clicked");

    const comments =
    document.getElementById(
    "comments-" + postId
    );

    comments.classList.toggle("show");
}