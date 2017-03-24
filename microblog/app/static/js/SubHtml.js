/**
 * 文件名：SubHtml.js
 * 作　者：DHC
 * 说　明：带HTML标签根据HTML内容截取指定长度的HTML文本，并自动补齐截取后的标签
 * 版　本：1.0
 * 时　间：2014-02-24
 * 示　例：subHtml($("#div715").html(), 73, false)
 */
(function(o){
    /**
     * 判断数组中是否包含某个元素
     */
    Array.prototype.inArray = function(v){
        for(i=0; i < this.length; i++) {
            if(this[i] == v){
                return true;
            }
        }
        return false;
    }
    
    /**
     * 将HTML字符串里面的文本字符检出
     */
    o.toText = function(oHtml){
        if(typeof oHtml === "string"){
            return oHtml.replace(/(^\s*)|(\s*$)/g, "").replace(/<[^<^>]*>/g, "").replace(/[\r\n]/g, "");
        } else {
            return "";
        }
    };
    
    /**
     * 截取带HTML样式的字符串，并保留并自动补齐HTML标签
     * oHtml  将要截取的HTML字符串
     * nlen   截取后的长度，包含标签之间的空格
     * isByte 是否按照字节长度截取
     */
    o.subHtml = function(oHtml, nlen, isByte){
        var rgx1 = /<[^<^>^\/]+>/;      //前标签(<a>的href属性中可能会有“//”符号，先移除再判断)
        var rgx2 = /<\/[^<^>^\/]+>/;    //后标签
        var rgx3 = /<[^<^>^\/]+\/>/;    //自标签
        var rgx4 = /<[^<^>]+>/;         //所有标签
        var selfTags = "hr,br,img,input,meta".split(",");
        if(typeof oHtml !== "string"){
            return "";
        }
        oHtml = oHtml.replace(/(^\s*)|(\s*$)/g, "").replace(/[\r\n]/g, "");
        var oStr = oHtml.replace(/<[^<^>]*>/g, "");
        var olen = isByte ? oStr.replace(/[^\x00-\xff]/g,"**").length : oStr.length;
        if(!/^\d+$/.test(nlen) || olen <= nlen){
            return oHtml;
        }
        var tStr = oHtml;
        var index = 0;
        var matchs = new Array();
        while(rgx4.test(tStr)){
            var m = new Object();
            m.index = index + tStr.search(rgx4);
            m.string = tStr.match(rgx4).toString();
            var len = tStr.search(/<[^<^>]+>/)+tStr.match(/<[^<^>]+>/)[0].length;
            tStr = tStr.substr(len);
            index += len;
            matchs.push(m);
        }
        if(isByte){
            var i=0;
            for(var z = 0; z < oStr.length; z++){
                i += (oStr.charCodeAt(z) > 255) ? 2 : 1;
                if(i >= nlen){
                    tStr=oStr.slice(0,(z + 1));
                    break;
                }
            }
        } else {
            tStr = oStr.substr(0, nlen);
        }
        var startTags = new Array();
        for(var i = 0; i < matchs.length; i++){
            if(tStr.length <= matchs[i].index){
                //tStr += matchs[i].string;
                matchs = matchs.slice(0, i);
                break;
            } else {
                tStr = tStr.substring(0, matchs[i].index) + matchs[i].string + tStr.substr(matchs[i].index);
                if(rgx1.test(matchs[i].string.replace(/(\/\/)/g, ""))){
                    var name = matchs[i].string.replace(/[<>]/g, "").split(" ");
                    if(name.length > 0){
                        name = name[0];
                        if(!selfTags.inArray(name)){
                            startTags.push(name);
                        }
                    }
                } else if(rgx2.test(matchs[i].string)){
                    var name = matchs[i].string.replace(/[<\/>]/g, "");
                    if(startTags.length > 0 && startTags[startTags.length - 1] === name){
                        startTags.pop();
                    }
                }
            }
        }
        if(startTags.length > 0){
            for(var i = startTags.length - 1; i >=0; i--){
                tStr += '</' + startTags[i] + '>';
            }
        }
        return tStr;
    }
}(window));