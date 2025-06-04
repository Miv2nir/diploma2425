export function validateForm(form){
    var values_missing=false;
    for (var i in form){
        if (form[i]!=null){
            if (form[i].required==true){
                //check if filled
                console.log(form[i]);
                if (!form[i].value){
                    form[i].labels[0].classList.add('error-text');
                    values_missing=true;
                }
                else{
                    form[i].labels[0].classList.remove('error-text');
                }
                
                
            }
        }
    }
    return values_missing;
}