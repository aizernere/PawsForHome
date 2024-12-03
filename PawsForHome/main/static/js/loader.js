
  document.addEventListener("DOMContentLoaded", () => {
    const loader = document.getElementById("page-loader");
    const content = document.getElementById("content");

    window.addEventListener("pageshow", function (event) {
        if (event.persisted) {
            // If the page is loaded from cache, skip the loader
            content.classList.remove("fade-in");
            loader.style.display = "none";
            content.style.display = "block";
            setTimeout(() => {
                content.classList.add("fade-in");
              }, 100);
        } else {
            window.addEventListener("beforeunload", () => {
                loader.classList.add("active");
                content.style.display = "none";
              });
        
            setTimeout(() => {
                loader.classList.remove("active");
                content.style.display = "block";  
                setTimeout(() => {
                  content.classList.add("fade-in");
                }, 50);
                 
            }, 500); 
        }
    });

    


});


