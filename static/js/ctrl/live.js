/*
61 word
62 note
*/

(function() {
	var feed_loader = feed_load_maker( "id rt_list"),
	DATE_ATTR = "zsite_cid zsite_name zsite_link unit title pic".split(' ');

	function array2zsite(a) {
		return {
			name: a[0],
			link: a[1]
		}
	}

	function init(result, site_dict) {
		var data = {
			"item": []
		},
		i = 0,
		j,
		attr,
		item = result[6],
		t,
		rt_list,
        site_id;

		for (; i < DATE_ATTR.length; ++i) {
			data[DATE_ATTR[i]] = result[i]
		}


		for (i = 0; i < item.length; ++i) {
            t = feed_loader(item[i]);

			rt_list = t.rt_list;
			if (rt_list.length) {
				if (! (rt_list.length == 1 && rt_list[0][0] == 0)) {
					t.rt_list = []
					for (j = 0; j < rt_list.length; ++j) {
						if (rt_list[j][0]) {
							t.rt_list.push(rt_list[j])
						}
					}
					t.rt_list = $.map(t.rt_list, array2zsite);
				} else {
					t.rt_list = [0]
				}
			}

			t.create_time = $.timeago(t.create_time);
            
            site_id = t.site_id;
            if(site_id){
                t.site_name = site_dict[site_id];
                t.site_url = site_id+HOST_SUFFIX
            }
			data.item.push(t)	
		}
		return data
	}

	function init_result(result) {
		var site_dict = result.pop(),
        length = result.length,
		item = [],
		i = 0,
		data,
		pre_zsite_id;

		for (; i < length; ++i) {
			data = init(result[i], site_dict)
			if (data.zsite_id == pre_zsite_id) {
				data.zsite_same_as_pre = true
			} else {
				pre_zsite_id = data.zsite_id
			}
			item.push(data)
		}
        
		return item
	}
    feed_page(
        "/j/feed/", "#feeds" , init_result, function(){
			var prebottom, top, diff, self;
			$("#feeds .G3").each(function() {
				self = $(this)
				top = self.offset().top;
				if (self.hasClass('G3_AS_PRE') && prebottom !== undefined) {
					diff = prebottom - top
					if (diff) {
						this.style.marginTop = diff + "px"
					}
				}
				prebottom = self.offset().top + this.offsetHeight;
			})
        }
    )

	/* 发微博 */
	var po_word_txt = $("#po_word_txt"),
	po_word_txt_bg = "po_word_txt_bg";
	po_word_txt.blur().val('').focus(function() {
		this.className="po_word_txt"
	}).blur(function() {
		var self = $(this),
		val = self.val();
		if (!val || ! val.length) {
			self.addClass(po_word_txt_bg)
		}
	}).addClass(po_word_txt_bg);
    
    function po_all_show_ext_hide(){
            po_all.show()
            po_ext.hide()
    }
    var po_all=$("#po_all"),po_ext=$('<a href="javascript:void(0)" id="po_ext"></a>').click(po_all_show_ext_hide);
    po_all.after(po_ext)
	$("#po_word_form").submit(
        txt_maxlen(
            po_word_txt, 
            $("#po_word_tip"), 
            142, 
            function(){
                po_all.hide()
                po_ext.show()
            },
            po_all_show_ext_hide
        )
    )

    
    var txt = $('#po_word_txt')
    function recover(){
        txt.removeAttr('disabled')
        $('.btnw').show() 
        $('.po_loading').remove()
        $('#po_all').show() 
    }
    $(recover) 
    
    $('#po_word_form').submit(function(){
        var val = txt.val(),btn=$('#po_word_btn'); 
        if($.trim(val)=='')return false;
        $('#po_ext, #po_word_tip').hide()

        btn.append('<div class="po_loading"></div>')
        btn.find('button').blur() 

        txt.attr('disabled',true)
        $('.btnw').hide()
        $.postJSON(
            '/j/po/word',
            {
                "txt":val
            },
            function(result){
                recover()
                if(result){
                    $('#feed').tmpl(init_result(result)).prependTo("#feeds")
                }
                txt.val('').attr('disabled',false).attr("class","po_word_txt po_word_txt_sayed")
                 
            }
        )
        return false
    })   


})()


pop_hero = function(elem){
    elem.live('mouseover',function(){
        var self = $(this)
        $.postJSON('j/hero',{url:self.attr('href')},function(result){
            var title = result[1].split()
            if(!$('.pop_hero')[0]){
                $('body').prepend('<div class="pop_hero"><div class="pop_hero_to"></div><a href="//'+result[6]+'.42qu.com"><img class="pop_hero_avatar" src="'+result[2]+'"></a><a href="//'+result[6]+'.42qu.com" class="pop_hero_name">'+result[0]+'</a><div class="pop_hero_bio">'+title[0]+'<span class="pop_hero_title">'+title[1]+'</span></div><div class="pop_hero_banner"><div class="pop_hero_num">'+result[3]+'人关注</div><a href="javascript:follow_a('+result[4]+');void(0)" id="follow_a'+result[4]+'" class="pop_hero_follow">'+result[5]+'</a></div></div>')
                $('.pop_hero').offset({top:self.offset().top-116,left:self.offset().left-30})
            }
        })
    }).live('mouseout',function(){
        var on = false
        var pop_hero_remove = function(){$('.pop_hero').remove()}
        clear_pop_hero = function(){
            if(!on){
                pop_hero_remove()
            }else{
                $('.pop_hero').bind('mouseleave',pop_hero_remove)
            }
        }
        $('.pop_hero').live('mouseover',function(){on = true}).unbind('mouseleave')
        setTimeout("clear_pop_hero()",200)
    })
}

pop_hero($('.fcmname'))

$('#po_word_txt').pop_at("/j/at")

