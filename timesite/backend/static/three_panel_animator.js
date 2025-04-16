//var init
    var container_left=document.getElementById('container-side-1');
    var container_main=document.getElementById('container-main');
    var container_right=document.getElementById('container-side-2');
    var animate=false;
    var shrunk=(window.innerWidth <1000);
    function addTransition() {
        container_left.classList.add('transitioning');
        container_right.classList.add('transitioning');
        container_main.classList.add('transitioning');
        console.log('transitions added');
    }
    function removeTransition() {
        container_left.classList.remove('transitioning');
        container_right.classList.remove('transitioning');
        container_main.classList.remove('transitioning');
        animate=false;
        console.log('transitions removed');
    }
    function delayedRemoveTransition(){
        //console.log('aea');
        setTimeout(removeTransition,100);
    }
    function hider() {
        if (window.innerWidth <1000) {
            if (animate==false && shrunk ==false){
                animate=true;
                shrunk=true;
                addTransition();
            }
            container_left.classList.add('hidden');
            container_right.classList.add('hidden');
            container_main.classList.add('full-width');
        }
        else {
            if (animate==false && shrunk ==true){
                animate=true;
                shrunk=false;
                addTransition();
            }
            container_left.classList.remove('hidden');
            container_right.classList.remove('hidden');
            container_main.classList.remove('full-width');
        }
        //window.addEventListener('resize',hider);
    }
    
    
    window.onresize = hider;
    //addEventListener('animationstart',(addTransition));
    addEventListener('transitionend',(delayedRemoveTransition));
    //fire the function on page load, otherwise it doesnt do anything on mobile unless form fields are interacted with
    hider();