# 利用Sanic 的基礎框架建立 Restful API / Blueprint 藍圖管理頁面
from sanic import Blueprint
from sanic.response import text
# 我們要把純list 改成 json 因此使用 json
import json
# jieba 結巴斷字系統
import jieba
# 分析關鍵字使用的結巴分析模組
import jieba.analyse

# 我們先預設在 sanic 框架進入時就初始化結巴系統要不然每次 POST 都會太慢
jieba.initialize()
jieba.enable_parallel(4)
# jieba.load_userdict(file_name)
# 主要頁面的進入點採用藍圖去註冊頁面
main = Blueprint('index')


# 主要頁面'/'的路由 decorator 拿來建立這個路由用,採用 async 去做不同步處理增加多使用速度
@main.route('/api', methods=['POST', 'GET'])
async def index(request):
    # 攔截 POST 如果不是 POST , who care?
    if request.method == 'POST':
        # 先抓 form 內的 string 欄位
        string = request.form.get('string')
        # 重要的斷字分析以及關鍵字分析
        # 使用 extract_tags 的演算做法以消除不重要的垃圾
        # topk = 就是最多取樣數據
        etstring = jieba.analyse.extract_tags(string, topK=20)
        # 使用 textrk 的演算做法以消除不重要的垃圾
        txstring = jieba.analyse.textrank(string, topK=20)
        #######
        # 一些基礎的演算原則 原則設計:
        # 優先採用 extract_tags 演算法
        # 確認都不是沒有詞語在進行進階比較
        # textrk 演算用在 extract_tags 不存在他存在的時候
        # textrk 跟 extract_tags 扣除相同的後發現前者的額外詞組較多時
        #######
        print('debug')
        if len(etstring) > 0 or len(txstring) > 0:
            if len(etstring) is 0 and len(txstring) > 0:
                return text(json.dumps(txstring))
            elif len(etstring) > 0 and len(txstring) is 0:
                return text(json.dumps(etstring))
            else:
                comparelist = set(etstring) & set(txstring)
                if len(comparelist) is 0:
                    return text(json.dumps(etstring))
                elif len(etstring) - len(comparelist) > len(
                        txstring) - len(comparelist):
                    return text(json.dumps(etstring))
                elif len(etstring) - len(comparelist) < len(
                        txstring) - len(comparelist):
                    return text(json.dumps(txstring))
                else:
                    return text(json.dumps(etstring))
        else:
            return text(json.dumps(etstring))

    else:
        return text('Gone!')
