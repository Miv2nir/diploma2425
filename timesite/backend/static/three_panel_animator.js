//var init
    var container_left=document.getElementById('container-side-1');
    var container_main=document.getElementById('container-main');
    var container_right=document.getElementById('container-side-2');

    //var sidebar_substituter_left=document.getElementById('sidebar_substituter_left');

    var animate=false; //not a flag to set but a thing used in functions below
    var shrunk=(window.innerWidth <1000);

    var button_pressed_left=false;
    var button_pressed_right=false;

    var sidepanel_button_left = document.getElementById('sidepanel_button_left');
    var sidepanel_button_right = document.getElementById('sidepanel_button_right');
    var sidepanel_button_left_double = document.getElementById('sidepanel_button_left_double');
    var sidepanel_button_right_double = document.getElementById('sidepanel_button_right_double');

    //only for the editor
    var project_item=document.getElementById('project_item_editor');
    console.log(project_item);

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
        //console.log('transitions removed');
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
            sidepanel_button_left.classList.add('shown');
            sidepanel_button_right.classList.add('shown');
            sidepanel_button_left_double.classList.add('shown');
            sidepanel_button_right_double.classList.add('shown');
        }
        else {
            //remove left button press changes here
            button_pressed_left=false;
            //sidebar_substituter_left.classList.remove('triggered');
            container_left.classList.remove('unfold-left');
            //then the right ones
            button_pressed_right=false;
            container_right.classList.remove('unfold-right');
            if (animate==false && shrunk ==true){
                animate=true;
                shrunk=false;
                addTransition();
            }
            //
            //general process
            container_main.classList.remove('offset-left');
            container_main.classList.remove('offset-right');
            if (project_item!=null){
                project_item.classList.remove('offset-left');
                project_item.classList.remove('offset-right');
            }
            container_left.classList.remove('left');
            container_right.classList.remove('right');
            //setTimeout(function(){container_left.classList.remove('absoluted');},0);
            container_left.classList.remove('absoluted');
            container_right.classList.remove('absoluted');
            container_left.classList.remove('hidden');
            container_right.classList.remove('hidden');
            container_main.classList.remove('full-width');
            sidepanel_button_left.classList.remove('shown');
            sidepanel_button_right.classList.remove('shown');
            sidepanel_button_left_double.classList.remove('shown');
            sidepanel_button_right_double.classList.remove('shown');
        }
        //window.addEventListener('resize',hider);
    }
    function buttonPanelReturnLeft() { //called via onclick
        if (button_pressed_left){ //container hidden
            ////sidebar_substituter_left.classList.remove('triggered');
            addTransition();
            container_left.classList.add('hidden');
            container_left.classList.remove('unfold-left');
            button_pressed_left=false;
        }
        else { //container shown
            if (button_pressed_right) {
                buttonPanelReturnRight();
            }
            container_left.classList.add('absoluted');
            container_left.classList.add('left');
            //sidebar_substituter_left.classList.add('triggered');
            container_main.classList.add('offset-left');
            console.log(project_item);
            if (project_item!=null){
                project_item.classList.add('offset-left');
            }
            addTransition();
            container_left.classList.remove('hidden');
            container_left.classList.add('unfold-left');
            button_pressed_left=true;
        }
    }
    function buttonPanelReturnRight() { //called via onclick
        if (button_pressed_right){ //container hidden
            ////sidebar_substituter_right.classList.remove('triggered');
            addTransition();
            container_right.classList.add('hidden');
            container_right.classList.remove('unfold-right');
            button_pressed_right=false;
        }
        else { //container shown
            if (button_pressed_left) {
                buttonPanelReturnLeft();
            }
            container_right.classList.add('absoluted');
            container_right.classList.add('right');
            //sidebar_substituter_right.classList.add('triggered');
            container_main.classList.add('offset-right');
            if (project_item!=null){
                project_item.classList.add('offset-right');
            }
            addTransition();
            container_right.classList.remove('hidden');
            container_right.classList.add('unfold-right');
            button_pressed_right=true;
        }
    }
    
    window.onresize = hider;
    //addEventListener('animationstart',(addTransition));
    addEventListener('transitionend',(delayedRemoveTransition));
    //fire the function on page load, otherwise it doesnt do anything on mobile unless form fields are interacted with
    hider();