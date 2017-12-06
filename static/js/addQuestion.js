/**
 * Created by supery on 2017/12/5.
 */

$('#addQuestion').click(function () {
    // s = '<div class="well well-lg"><button type="button" class="close" data-dismiss="modal" aria-label="Close" onclick="functiondel(this)"><span aria-hidden="true">&times;</span></button><h4 style="color:#777">问题1：</h4><div class="form-group"><label for="inputPassword" class="col-sm-2 col-md-2 control-label">问题：</label><div class="col-md-2"><textarea name="" id="" cols="5" rows="2" class="form-control" style="width: 600px"></textarea></div></div><div class="form-group"><label for="inputPassword" class="col-sm-2 control-label">类型：</label><div class="col-md-3"><select name="type_id" class="form-control types" style="width: 250px" onchange="selectchange(this)"><option value="1">打分(1~10分)</option><option value="2">单选</option><option value="3">建议</option></select></div><ul class="nav col-md-2 myhite"><li role="presentation" class="active"><a><span class="glyphicon glyphicon-plus" aria-hidden="true"></span>&nbsp;&nbsp;添加选项</a></li></ul></div></div>';
    s = '<div class="well well-lg"><button type="button" class="close" data-dismiss="modal" aria-label="Close" onclick="functiondel(this)"><span aria-hidden="true">&times;</span></button><h4 style="color:#777">添加问题</h4><div class="form-group"><label for="area" class="col-sm-2 col-md-2 control-label">问题：</label><div class="col-md-3"><textarea name="" id="" cols="5" rows="2" class="form-control" style="width: 600px"></textarea></div></div><div class="form-group"><label for="area" class="col-sm-2 col-md-2 control-label">类型：</label><div class="col-md-3"><select name="type_id" class="form-control types" style="width: 250px" onchange="selectchange(this)"><option value="1" >打分(1~10)</option><option value="2">单选</option><option value="3">建议</option></select></div><ul class="nav col-md-2 myhite addoption"><li role="presentation" class="active addSelect" onclick="addSelectfunc(this)"><a><span class="glyphicon glyphicon-plus " aria-hidden="true"></span>&nbsp;&nbsp;添加选项</a></li></ul></div><div class="col-md-offset-2 col-sm-offset-2"><ul class="form-inline" id="addop"></ul></div></div>';
    $('#Questions form').append(s)
});
/* 删除问题块*/
function functiondel(t) {
    $(t).parent().remove()
}

/* 获取到所有的select标签绑定绑定事件*/
function selectchange(select) {
    var val_id = $(select).children('option:selected').val();
    if (val_id == 2) {
        $(select).parent().next().removeClass('myhite')
    }
    else {
        var ele_ul = $(select).parent().parent().next().children('ul');
        ele_ul.children('li').remove();
        $(select).parent().next().addClass('myhite')
    }
}
/* 给添加选项绑定事件*/
function addSelectfunc(t) {
    // console.log(t);
    s = '<li>内容: <input type="text" class="form-control" value=""> &nbsp;&nbsp;  分值: <input type="text" class="form-control" value=""><button type="button" class="close" data-dismiss="modal" aria-label="Close" onclick="functiondel(this)"><span aria-hidden="true">&times;</span></button></li>';
    $(t).parent().parent().next().children('ul').append(s)
    // ele_ul.append(s);
    // $('.addoption').click(function () {
    //     s = '<li>内容: <input type="text" class="form-control" value=""> &nbsp;&nbsp;  分值: <input type="text" class="form-control" value=""><button type="button" class="close" data-dismiss="modal" aria-label="Close" onclick="functiondel(this)"><span aria-hidden="true">&times;</span></button></li>';
    //
    //     var ele_parent = $(t).parent();
    //     // var ele_parent = $(this).parent();
    //     var ele_ul = ele_parent.next().children('ul');
    //     ele_ul.append(s);
    // });
}











