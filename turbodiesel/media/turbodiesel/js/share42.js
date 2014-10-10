/* share42.com | 20.11.2012 | (c) Dimox */
window.onload = function () {
    d = document.getElementsByTagName('div');
    for (var i = 0; i < d.length; i++) {
        if (d[i].className.indexOf('share42init') != -1) {
            if (d[i].getAttribute('data-url') != -1)u = d[i].getAttribute('data-url');
            if (d[i].getAttribute('data-title') != -1)t = d[i].getAttribute('data-title');
            if (d[i].getAttribute('data-path') != -1)f = d[i].getAttribute('data-path');
            if (d[i].getAttribute('data-top1') != -1)m1 = d[i].getAttribute('data-top1');
            if (d[i].getAttribute('data-top2') != -1)m2 = d[i].getAttribute('data-top2');
            if (d[i].getAttribute('data-margin') != -1)m3 = d[i].getAttribute('data-margin');
            if (!f) {
                function path(name) {
                    var sc = document.getElementsByTagName('script'), sr = new RegExp('^(.*/|)(' + name + ')([#?]|$)');
                    for (var i = 0, scL = sc.length; i < scL; i++) {
                        var m = String(sc[i].src).match(sr);
                        if (m) {
                            if (m[1].match(/^((https?|file)\:\/{2,}|\w:[\/\\])/))return m[1];
                            if (m[1].indexOf("/") == 0)return m[1];
                            b = document.getElementsByTagName('base');
                            if (b[0] && b[0].href)return b[0].href + m[1]; else return document.location.pathname.match(/(.*[\/\\])/)[0] + m[1];
                        }
                    }
                    return null;
                }

                f = path('share42.js');
            }
            if (!u)u = location.href;
            if (!t)t = document.title;
            if (!m1)m1 = 150;
            if (!m2)m2 = 20;
            if (!m3)m3 = 0;
            u = encodeURIComponent(u);
            t = encodeURIComponent(t);
            t = t.replace('\'', '%27');
            var s = new Array('"#" onclick="window.open(\'http://www.facebook.com/sharer.php?u=' + u + '&t=' + t + '\', \'_blank\', \'scrollbars=0, resizable=1, menubar=0, left=200, top=200, width=550, height=440, toolbar=0, status=0\');return false" title="Поделиться в Facebook"', '"#" onclick="window.open(\'https://plus.google.com/share?url=' + u + '\', \'_blank\', \'scrollbars=0, resizable=1, menubar=0, left=200, top=200, width=550, height=440, toolbar=0, status=0\');return false" title="Поделиться в Google+"', '"#" onclick="window.open(\'http://www.odnoklassniki.ru/dk?st.cmd=addShare&st._surl=' + u + '&title=' + t + '\', \'_blank\', \'scrollbars=0, resizable=1, menubar=0, left=200, top=200, width=550, height=440, toolbar=0, status=0\');return false" title="Добавить в Одноклассники"', '"#" onclick="window.open(\'http://twitter.com/share?text=' + t + '&url=' + u + '\', \'_blank\', \'scrollbars=0, resizable=1, menubar=0, left=200, top=200, width=550, height=440, toolbar=0, status=0\');return false" title="Добавить в Twitter"', '"#" onclick="window.open(\'http://vk.com/share.php?url=' + u + '&title=' + t + '\', \'_blank\', \'scrollbars=0, resizable=1, menubar=0, left=200, top=200, width=554, height=421, toolbar=0, status=0\');return false" title="Поделиться В Контакте"', '"http://share42.com/" title="Share42.com - Бесплатный скрипт кнопок социальных закладок и сетей"');
            var l = '';
            for (j = 0; j < s.length; j++)l += '<a rel="nofollow" style="display:block;width:32px;height:32px;margin:0 0 6px;padding:0;outline:none;background:url(' + f + 'icons.png) -' + 32 * j + 'px 0 no-repeat" href=' + s[j] + ' target="_blank"></a>';
            d[i].innerHTML = '<span id="share42" style="position:fixed;z-index:9999;margin-left:' + m3 + 'px">' + l + '</span>';
            var p = document.getElementById('share42');

            function m() {
                var top = Math.max(document.body.scrollTop, document.documentElement.scrollTop);
                if (top + (m2 * 1) < m1) {
                    p.style.top = m1 - top + 'px';
                } else {
                    p.style.top = m2 + 'px';
                }
            }

            m();
            window.onscroll = m;
        }
    }
};