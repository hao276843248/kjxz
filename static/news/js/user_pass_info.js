$(function () {
    $(".pass_info").submit(function (e) {
        e.preventDefault();
        var params = {};
        $(this).serializeArray().map(function (x) {
            params[x.name] = x.value;
        });
        $.ajax({
            url: "/passHtml",
            type: "post",
            contentType: "application/json",
            data: JSON.stringify(params),
            success: function (resp) {
                $('.list_con').html('')
                for (var i = 0; i < resp.length; i++) {
                    var urls1 = resp[i].url
                    var name = resp[i].name
                    var del = '<a  href="'+urls1+'" target="_blank" class= "ia">下 载</a>'
                    var content = '<li>'
                    content += '<div class="news_detail">' + name + '</div>'
                    content += del
                    content += '</li>'
                    $(".list_con").append(content)
                }
            }
        })
    })

})
