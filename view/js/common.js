// メニュー設定
function setting_menu(){
    var navFlg = false;
    $('.menu').on('click', function () {
        $('.menu__line').toggleClass('active');
        $('.gnav').fadeToggle();
        if (!navFlg) {
            $('.gnav__menu__item').css({
                'margin-left': 100,
                'opacity': 0,
            });
            $('.gnav__menu__item').each(function (i) {
                $(this).delay(i * 300).animate({
                    'margin-left': 0,
                    'opacity': 1,
                }, 500);
            });
        }
        navFlg = !navFlg;
    });
}


// json形式データから<table>子要素のhtmlを生成する
function from_json_to_table(json){
    let table = "";
    // テーブルヘッダー作成
    table += "<thead class='red lighten-2'>\n";
    table += "<tr>\n";
    for (key in json[0]) {
        table += "<th>\n";
        table += key
        table += "</th>\n";
    }
    table += "</tr>\n";
    table += "</thead>\n";
    // テーブル本体作成
    table += "<tbody>\n";
    for (i = 0; i < json.length; i++) {
        table += "<tr>\n";
        for (key in json[i]) {
            table += "<td>";
            if (json[i][key] != null){
                table += json[i][key];
            }
            table += "</td>\n";
        }
        table += "</tr>\n";
    }
    table += "</tbody>\n";

    return table
}
