function autocomplete_tag(id, default_tag_list, idPrefix){
    var elem=$(id), t, i, 
        o = {
            onResult: function (results) {
                var list = [],
                    i=0, 
                    ctrl=0,
                    word = $('#'+o.idPrefix+'-tags').val();
        
                for(;i<results.length;++i){
                    t = results[i]
                    t = {
                        id:t[0],
                        name:t[2],
                        num:t[1]
                    }
                    if(t.name == word){
                        ctrl = 1 
                        list.unshift(t)
                    }else{
                        list.push(t)
                    }
                }
                if(ctrl)list.unshift({id:'-'+word,name:word,num:0})
                return list
            },
            propertyToSearch: "name",
            resultsFormatter: function(item){
                if(String(item.id).substring(0,1)=='-'){
                    return '<li class="dropdown_add">添加 "'+item.name+'" 标签</li>'
                }
                return '<li>'+item.name+'<span class="drop_follow_num">'+item.num+'人关注</span></li>'
            },
            tokenFormatter: function(item){
                 return '<li class="token-input-token"><p>'+item.name+'</p></li>'+'<input type="hidden" name="tag_id_list" value="'+item.id+'">' 
            }

        }
    if(idPrefix){
        o.idPrefix = idPrefix
    }
    elem.tokenInput("http://api"+HOST_SUFFIX+"/po/tag",o)
    
    if(default_tag_list.length){
        for(i=0;i<default_tag_list.length;++i){
            t=default_tag_list[i]
            elem.tokenInput("add", {id: t[1], name: t[0]});
        }
    }
}