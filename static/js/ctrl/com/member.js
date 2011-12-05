$(function(){
    $('.search_input').focus()
    $('.f_item').toggle(
        function(){ 
            $(this).toggleClass('f_item2')
            $(this).toggleClass('f_item')
        },
        function(){ 
            $(this).toggleClass('f_item2')
            $(this).toggleClass('f_item')
        })
    $('#select_all').click(
        function(){
            if($(this).attr('checked')){
                $('.f_item').attr('class','f_item2')
            } else{
                $('.f_item2').attr('class','f_item')
            }
        }
    )

    $("#follow_form").submit(function(){
        var select_ids = [];

        $('.f_item2').each(function(){
            select_ids.push(this.id)
        })

        $("#follow_id_list").val(select_ids.join(' '))
        
    })

auto_add('member_mail','<div class="line"><input placeholder="邮箱" name="mail" class="member_mail"><input placeholder="姓名" name="name" class="member_name"></div>','mail_block','','focus')

auto_add('member_mail_short','<div class="line"><input placeholder="邮箱" name="mail" class="member_mail_short"><input placeholder="姓名" name="name" class="member_name_short"></div>','mail_block','','focus')

auto_add('member_link','<div class="line"><input class="member_link" name="link" placeholder="用户网址"></div>','link_block','','focus')


    $('.member_rm_a').click(function(){
        var self = $(this)
        var url = self.attr('id').split('_')[0]=='in'?'':'/invite'
        var id = self.attr('id').split('_')[1]
        self.parent().remove()
        $.postJSON("/j/member" +url+"/rm/"+id) 
    })

})

