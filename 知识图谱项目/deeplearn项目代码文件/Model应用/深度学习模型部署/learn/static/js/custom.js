// 封装弹窗layer组件等
var common_ops = {
  alert:function( msg ,cb ){
      layer.alert( msg,{
          yes:function( index ){
              if( typeof cb == "function" ){
                  cb();
              }
              layer.close( index );
          }
      });
  },
  confirm:function( msg,callback ){
      callback = ( callback != undefined )?callback: { 'ok':null, 'cancel':null };
      layer.confirm( msg , {
          btn: ['确定','取消'] //按钮
      }, function( index ){
          //确定事件
          if( typeof callback.ok == "function" ){
              callback.ok();
          }
          layer.close( index );
      }, function( index ){
          //取消事件
          if( typeof callback.cancel == "function" ){
              callback.cancel();
          }
          layer.close( index );
      });
  },
  tip:function( msg,target ){
      layer.tips( msg, target, {
          tips: [ 3, '#e5004f']
      });
      $('html, body').animate({
          scrollTop: target.offset().top - 10
      }, 100);
  }
};
$(function () {
        var trainBtn = $('#trainBtn');
        var paraBtn = $('#paraBtn');
        var testBtn = $('#testBtn');
        var addBtn = $('#addBtn');
        var useBtn = $('#useBtn');


        paraBtn.on('click', function () {
                paraBtn.attr('disabled',true);
                //获取超参数的值
                var path = $('#path').val();
                var model_path = $('#model_path').val();
                var n_step_in = $('#n_step_in').val();
                var n_step_out = $('#n_step_out').val();
                var column = $('#column').val();
                var predict = $('#predict').val();
                var batch_size = $('#batch_size').val();
                var epochs = $('#epochs').val();
                // 上传数据
                // data是JavaScript对象，而不是json字符串
                var data={};
                data["path"] = path;
                data["model_path"] = model_path;
                data['n_step_in'] = n_step_in;
                data['n_step_out'] = n_step_out;
                data['column'] = column;
                data['predict'] = predict;
                data['batch_size'] = batch_size;
                data['epochs'] = epochs;

                // data转为json字符串
                var jsonString = JSON.stringify(data)
                 $.ajax({
                      url: '/train_para',
                      method: 'POST',
                      data: jsonString,
                      //在 AJAX 请求中设置 contentType: 'application/json'，告诉服务器发送的数据类型是 JSON 格式的字符串。
                      //这样，服务器就能正确地解析请求中的 JSON 数据了
                      contentType: 'application/json',
                      success: function(res) {
                           // 收到回复，让按钮可点击
                            paraBtn.attr('disabled',false);
                            setTimeout(function(){
                                    alert('超参数修改成功!');
                                }, 100);

                          },
                          error: function() {
                            paraBtn.attr('disabled',false);
                            setTimeout(function(){
                                    alert('超参数修改失败!');
                                }, 100);
                          }
                   });
        });

        //点击训练
        trainBtn.on('click', function () {
                //不可点击按钮
                trainBtn.attr('disabled',true);
                $('.progress-bar').css('width','0%');
                // 设置定时器,隔段时间请求一次数据
                var sitv = setInterval(function(){
                    $.getJSON('/train_progress', function(num_progress){
                    //修改进度条
                        $('.progress-div').css('visibility', 'visible');
                        $('.progress-bar').css('width', num_progress.res + '%');
                        $('.progress-bar').css('background', 'green');
                        $('.progress-bar').css('text-align', 'center');
                        $('.progress-bar').text(num_progress.res + '%');
                        if(num_progress>=100){
                            $('.progress-bar').css('width', '100%');
                            $('.progress-bar').text('100%');
                         // 清除定时器
                            clearInterval(sitv);
                        }
                    });
                }, 500);
            // 点击事件请求地址，发送请求，后台业务开始执行
            var this_url = '/train_run'
            $.getJSON(this_url, function(res){
                // 清除定时器
                clearInterval(sitv);

                if(res != null){
                    $('.progress-bar').css('width', '100%');
                    $('.progress-bar').text('100%');
                    // 选择页面中的一个 id 为 plot-container 的 HTML 元素
                    $('#plot-container').html(res.plot_html);
                    // 可以点击按钮
                    trainBtn.attr('disabled',false)
                    setTimeout(function(){
                        alert('模型训练成功!');
                    }, 100);
                }else{
                    $('.progress-bar').css('background', 'red');
                     // 可以点击按钮
                    trainBtn.attr('disabled',false)
                    setTimeout(function(){
                        alert('模型训练失败了!');
                    }, 1);
                }
            });
        });
        testBtn.on('click', function () {
                testBtn.attr('disabled',true);
                $.getJSON('test_run', function(res){
                if(res != null){
                    // 选择页面中的一个 id 为 plot-container 的 HTML 元素
                    $('#test-img-container').html(res.plot_html);
                    $('#RMSE').text("RMSE: " +res.rmse);
                    $('#MAPE').text("MAPE: " +res.mape);
                    // 可以点击按钮
                    testBtn.attr('disabled',false)
                    setTimeout(function(){
                        alert('模型测试成功!');
                    }, 100);
                }else{
                     // 可以点击按钮
                    testBtn.attr('disabled',false)
                    setTimeout(function(){
                        alert('模型测试失败了!');
                    }, 100);
                }
            });
        });



layui.use('form', function() {
       //每个输入框和删除按钮的HTML结构都被包裹在一个独立的div容器中，以便单独操作
       //通过点击对应输入框的删除按钮，可以删除该输入框及其容器，而不会影响其他输入框
       var form = layui.form;
      // 添加输入框
      $("#addInput").on('click', function () {
        var count = $(".layui-form-item").length; // 获取输入框数量
        // count是设置属性值，属性值计算是原有输入框数量-1
        count =count -1;
        var html = '<div class="layui-form-item">' +
          '<div class="layui-input-inline">' +
          '<input type="text" name= "input_' + count +'" placeholder="param_' + count + '" class="layui-input">' +
          '</div>' +
          '<div class="layui-input-inline">' +
          '<button class="layui-btn layui-btn-danger layui-btn-primary deleteInput" type="button">delete</button>' +
          '</div>' +
          '</div>';
        $("#inputContainer").append(html);
        form.render(); // 重新渲染表单元素
      });

      // 删除输入框
      $(document).on('click', '.deleteInput', function () {
        $(this).parents('.layui-form-item').remove();
        form.render(); // 重新渲染表单元素
      });
        var times = 1
      // 监听表单提交
      form.on('submit(submitForm)', function(data) {

         $("#subBtn").attr('disabled',true);
          $('#prediction').text('开始测试——'+times);
           times = times + 1;
        var formData = data.field;
          // 循环遍历表单字段，并将值转换为浮点数类型
          for (var key in formData) {
            if (formData.hasOwnProperty(key)) {
              formData[key] = parseFloat(formData[key]);
            }
          }
        $.ajax({
          url: '/use_run',
          type: 'POST',
          data: formData,
          success: function (res) {
            $("#subBtn").attr('disabled',false);
            // 处理返回结果，更新预测值
            if(res!=null){
            // 解析 JSON 字符串为 JavaScript 对象
            var dict = JSON.parse(res);
            // 构建 layui的HTML 内容
            var htmlContent = '<table class="layui-table"><colgroup><col width="200"><col></colgroup><tbody>';
            for (var key in dict) {
              if (dict.hasOwnProperty(key)) {
                var value = dict[key];
                htmlContent += '<tr><td>' + key + '</td><td>' + value + '</td></tr>';
              }
            }
            htmlContent += '</tbody></table>';
            // 将 HTML 内容插入到页面中
            var dictionaryContainer = document.getElementById("dictionary");
            dictionaryContainer.innerHTML = htmlContent;
            setTimeout(function(){
                        alert('预测成功!');
                    }, 100);
            }
            else{
                $("#subBtn").attr('disabled',false);
                    setTimeout(function(){
                        alert('预测失败了!');
                    }, 100);
                }
          },
          error: function() {
                            setTimeout(function(){
                                    alert('预测失败了!');
                                }, 100);
       }
        });
      });
      return false; // 阻止表单默认提交
    });

});






