/**
 * Created by supery on 2017/11/20.
 */

// 先清除报错信息
$(".pull-right").html(' ');
$(".pull-right").parent().removeClass('has-error');

// 头像预览
$("#avatar_file").change(function () {
    var ele_file=$(this)[0].files[0];
    var reader = new FileReader();
    reader.readAsDataURL(ele_file);     // 读取当前数据的url
    reader.onload=function () {
        $("#avatar_img")[0].src=this.result
    }

});


$("#reg_btn").click(function () {
    var formData = new FormData();

    var email = $("#id_email").val();
    var tel = $("#id_tel").val();
    var username = $("#id_username").val();
    var password = $("#id_password").val();
    var repeat_pwd = $("#id_repeat_pwd").val();
    var nickname = $("#id_nickname").val();
    var avatar_file = $("#avatar_file")[0].files[0];
    console.log(avatar_file);
    formData.append("username", username);
    formData.append("password", password);
    formData.append("repeat_pwd", repeat_pwd);
    formData.append("nickname", nickname);
    formData.append("email", email);
    formData.append("tel", tel);
    formData.append("avatar_file", avatar_file);

    $.ajax({
        url: "/reg/",
        type: 'POST',
        headers: {"X-CSRFToken": $.cookie('csrftoken')},
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
            console.log(data);
            var data=JSON.parse(data);
            if (data.user){
                location.href='/login/'
            }
            else{
                // console.log(data.errorList);
                $.each(data.errorList,function (i,j) {
                    console.log(i,j);
                    $span=$("<span>");
                    $span.addClass("pull-right").css("color",'red');
                    $span.html(j[0]);
                    $("#id_"+i).after($span).parent().addClass("has-error");
                    if(i=="__all__"){
                        $("#id_repeat_pwd").after($span)
                    }
                })
            }

        }
    })
});
