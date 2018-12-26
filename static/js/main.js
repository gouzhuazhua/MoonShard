$(document).on('readystatechange', function () {
    NProgress.start();
    // alert("state:" + document.readyState);
    console.log(document.readyState);
    if(document.readyState == "Uninitialized"){
        NProgress.set(1);
    }
    if(document.readyState == "Interactive"){
        NProgress.set(0.5);
    }
    if(document.readyState == "complete"){
        NProgress.done();
    }
});