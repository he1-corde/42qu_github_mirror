rm = _rm("#reply","/po/reply/rm/")
$(function(){$(".G,.G4").css('position','static')})
$("#txt_form").elastic_login()
$(".reply_at").live("click", function(){
    var txt=$("#reply_txt").focus(),
        val=txt.val(),
        name=$(this.parentNode).find(".replyer").text(),
        add;
    add =  "@"+name+'('+this.rel+') '
    if(val.length){
        if($.trim(val)==val){
            val+=" "
        }
        val+=add;
    }else val=add;

    txt.val(val)

    $("#reply_txt").pop_at("/j/at/reply/"+$('#txt_form').attr('action').split('/')[3],27)
})
$("#reply_txt").elastic()
if(!IE6){
    $(function(){
        var st = $('#sT');
        if(st[0]){
            st.css('position','absolute')
            var top = st.offset().top, win=$(window).scroll(function() {
                if(win.scrollTop() >= top-16){
                    st.css({'position':'fixed',"marginTop":"-56px"})
                }else{
                    st.css({'position':'absolute',"marginTop":"36px"})
                }
            })
        }

    })
}
$(function(){
    codesh()
    if($(window).width()<827){
        $(".sprev,.snext").hide()
        
    }
});

(function(){

    var INPUT_FOCUS;
    
    $(document).keyup(function (e) {
        if (!INPUT_FOCUS && !(e.ctrlKey || e.shiftKey || e.altKey) ) {
            var id
            switch (e.keyCode) {
                case 37://←
                id="sprev"
                break
                case 39://→
                id="snext"
                break
            }
            if(id){
                id = $('.'+id)[0]
                if(id){
                    location = id.href
                }
            }
        }
    })
    
    function input_ban () {
        $('input, textarea').live('focus',function () {
            INPUT_FOCUS = this
        }).live('blur',function () {
            INPUT_FOCUS = null
        })
    }
    $(input_ban)
    $(document).ajaxComplete(input_ban)

})();

