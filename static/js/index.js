/**
 * Created by supery on 2017/11/22.
 */


/* 添加文件调查问卷*/
$('#save').click(function () {
   $.ajax({
       url:'addqs/',
       type:'post',
       data:{
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            title:$("#question").val(),
            select_val:$("#qs_classes option:selected").val()
       },
       success:function (data) {
           var data=JSON.parse(data);
           console.log(data.add_msg);
           if(data.add_msg){

           }
       }
   })

});

/* 删除文件调查问卷*/
$(".del_qs").click(function () {
    var qs_id=$(this).attr('qs_id');
    var qs_tr=$(this).parent().parent();
   $.ajax({
       url:'/delqs/',
       type:'post',
       data:{
           csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
           qs_id:qs_id
       },
       success:function (data) {

           var data=JSON.parse(data);
           if (data.del_msg){
               qs_tr.remove()
           }
       }
   })
});









