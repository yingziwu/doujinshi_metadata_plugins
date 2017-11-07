#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__   = 'GPL v3'
__copyright__ = '2017, Wu Yuan <i@a3s.site>'
__docformat__ = 'restructuredtext en'

from calibre.ebooks.metadata.sources.base import Source, Option
from calibre.ebooks.metadata.book.base import Metadata
from calibre import as_unicode

import re
import json
from urllib import urlencode

def to_metadata(log,gmetadata,ExHentai_Status,translate_tag): # {{{
    title = gmetadata['title']
    title_jpn = gmetadata['title_jpn']
    tags = gmetadata['tags']
    rating = gmetadata['rating']
    category = gmetadata['category']
    gid = gmetadata['gid']
    token = gmetadata['token']
    thumb = gmetadata['thumb']
    
    # title
    if title_jpn:
        raw_title = title_jpn
    else:
        raw_title = title
    pat1 = re.compile(r'(?P<comments>.*?\[(?P<author>(?:(?!汉化|漢化)[^\[\]])*)\](?:\s*(?:\[[^\(\)]+\]|\([^\[\]\(\)]+\))\s*)*(?P<title>[^\[\]\(\)]+).*)')
    if re.findall(pat1,raw_title):
        m = re.search(pat1, raw_title)
        title_ = m.group('title').strip()
        author = m.group('author').strip()
    else:
        title_ = raw_title.strip()
        author = 'Unknown'
        log.exception('Title match failed. Title is %s' % raw_title)
    
    authors = [(author)]
        
    mi = Metadata(title_, authors)
    mi.identifiers = {'ehentai':'%s_%s_%d' % (str(gid),str(token),int(ExHentai_Status))}
    
    # publisher
    pat2 = re.compile(r'^\(([^\[\]\(\)]*)\)')
    if re.findall(pat2, raw_title):
        publisher = re.search(pat2, raw_title).group(1).strip()
        mi.publisher = publisher
    else:
        mi.publisher = 'Unknown'
        log.exception('Not Found publisher.')

    # Tags
    tags_ = []
    for tag in tags:
        if re.match('language',tag):
            tag_ = re.sub('language:','',tag)
            if tag_ != 'translated':
                mi.language = tag_
            else:
                tags_.append(tag_)
#         elif re.match('parody|group|character|artist', tag):
#             log('drop tag %s' % tag)
#             continue
        elif not ':' in tag:
            log('drop tag %s' % tag)
            continue
        else:
            tags_.append(tag)
    tags_.append(category)
    mi.tags = tags_ if not translate_tag else translate_tags(tags_)
    
    # rating
    mi.rating = float(rating)
    
    # cover
    mi.has_ehentai_cover = None
    if thumb:
        mi.has_ehentai_cover = thumb
    return mi
    # }}}

def translate_tags(tags):
    zh_json = {"3d":u"3D","=Age=":u"=年龄=","=Animal=":u"=动物=","=Arms=":u"=手臂=","=Bodily Fluids=":u"=体液=","=Body=":u"=身体=","=Bondage=":u"=束缚=","=Breasts=":u"=乳房=","=Buttocks=":u"=臀部=","=Change=":u"=变化=","=Chest=":u"=胸部=","=Contextual=":u"=语境=","=Cosplay=":u"=Cosplay=","=Costume=":u"=服饰=","=Creature=":u"=生物=","=Crotch=":u"=裆部=","=Disability=":u"=残疾=","=Either Hole=":u"=任何洞=","=Expunging=":u"=Expunging=","=Eyes=":u"=眼睛=","=Feet=":u"=脚部=","=Female=":u"=女性=","=Fluids=":u"=流体=","=Force=":u"=强迫=","=Head=":u"=头部=","=Height=":u"=身高=","=Incest=":u"=乱伦=","=Infidelity=":u"=不贞=","=Inter-gender Relations=":u"=跨性别关系=","=Language=":u"=语言=","=Legs=":u"=腿部=","=Lower Body=":u"=下身=","=Male Futanari Shemale=":u"=男性\\扶她\\人妖=","=Mouth=":u"=嘴部=","=Multiple Activities=":u"=多人性行为=","=Multiple Holes=":u"=多个洞=","=Neck=":u"=脖子=","=Nipples=":u"=乳头=","=Nose=":u"=鼻子=","=Privacy=":u"=隐私=","=Sadomasochism=":u"=虐恋=","=Self Pleasure=":u"=自慰=","=Semen=":u"=精液=","=Semi-Expunging=":u"=Semi-Expunging=","=Skin=":u"=皮肤=","=Technical=":u"=技术=","=Tools=":u"=工具=","=Torso=":u"=躯干=","=Violence=":u"=暴力=","=Waste=":u"=排泄物=","=Weight=":u"=体重=","=精神=":u"=意识=","abortion":u"堕胎","absorption":u"吞噬吸收","age progression":u"快速成长","age regression":u"返老还童","ahegao":u"阿黑颜","albanian":u"阿尔巴尼亚语","albino":u"白化","alien":u"外星人","alien girl":u"外星女","all the way through":u"头尾贯通","already uploaded":u"已上传过","amputee":u"人棍","anaglyph":u"立体","anal":u"肛交","anal birth":u"肛门生育","angel":u"天使","animal on animal":u"动物X动物","animal on furry":u"人型兽X动物","animated":u"动画","anorexic":u"骨瘦如柴","anthology":u"选集","apron":u"围裙","arabic":u"阿拉伯语","armpit licking":u"舔腋下","armpit sex":u"腋下交","artbook":u"画集","asphyxiation":u"窒息","ass expansion":u"屁股膨大","assjob":u"摩擦肛门","aunt":u"姨姑","autofellatio":u"自己口交","autopaizuri":u"自己乳交","ball sucking":u"吸奶子","balljob":u"睾丸交","balls expansion":u"睾丸膨大","bandages":u"绷带","bandaid":u"创可贴","bbm":u"胖帅男","bbw":u"胖美女","bdsm":u"施虐受虐","bear":u"熊","bee girl":u"蜂娘","bestiality":u"兽交","big areolae":u"大乳晕","big ass":u"大屁股","big balls":u"大睾丸","big breasts":u"巨乳","big clit":u"大阴蒂","big lips":u"大嘴唇","big nipples":u"大乳头","big penis":u"大阴茎","big vagina":u"大阴道","bike shorts":u"自行车短裤","bikini":u"比基尼","birth":u"出产","bisexual":u"双性恋","blackmail":u"勒索","blind":u"瞎子","blindfold":u"遮眼","blood":u"血液","bloomers":u"运动短裤","blowjob":u"口交","blowjob face":u"口交脸","body modification":u"身体改造","body painting":u"人体彩绘","body swap":u"身体交换","body writing":u"身上写字","bodystocking":u"连身袜","bodysuit":u"紧身衣","bondage":u"捆绑","braces":u"牙套","brain fuck":u"脑交","breast expansion":u"乳房膨大","breast feeding":u"母乳喂养","breast reduction":u"乳房缩小","bride":u"新娘","brother":u"兄弟","bukkake":u"颜射","bull":u"公牛","bunny boy":u"男兔人","bunny girl":u"兔娘","burping":u"打嗝","business suit":u"商务装","butler":u"男管家","camel":u"骆驼","cannibalism":u"同类相食","caption":u"无对话","cashier":u"收银员","cat":u"猫","catalan":u"加泰罗尼亚语","catboy":u"男猫人","catfight":u"两女相争","catgirl":u"猫娘","cbt":u"虐睾丸","centaur":u"半人马","cervix penetration":u"子宫脱出","chastity belt":u"贞操带","cheating":u"NTL睡别人爱人","cheerleader":u"拉拉队","chikan":u"痴汉","chinese":u"汉语","chinese dress":u"中式服装","chloroform":u"迷药","christmas":u"圣诞装","clit growth":u"阴蒂增长","coach":u"教练","cockslapping":u"阴茎蹭脸","collar":u"项圈","compilation":u"禁止的编辑","condom":u"避孕套","conjoined":u"连体","coprophagia":u"食粪","corruption":u"堕落","corset":u"紧身胸衣","cosplaying":u"Cos装","cousin":u"表姐/妹","cow":u"牛","cowgirl":u"奶牛娘","cowman":u"男奶牛人","crab":u"蟹","crossdressing":u"异性服装","crotch tattoo":u"胯部纹身","cum bath":u"泡精液浴","cum in eye":u"眼射","cum swap":u"交换精液","cunnilingus":u"舔阴","cuntboy":u"有屄的男人","czech":u"捷克语","dakimakura":u"抱枕","danish":u"丹麦语","dark nipples":u"黑乳头","dark sclera":u"暗色巩膜","dark skin":u"黑皮肤","daughter":u"女儿","deepthroat":u"深喉","defloration":u"破处","demon":u"恶魔","demon girl":u"女恶魔","diaper":u"尿布","dick growth":u"阴茎增长","dickgirl on dickgirl":u"扶她X扶她","dickgirl on male":u"扶她X男人","dicknipples":u"乳头如屌","dilf":u"熟男","dinosaur":u"恐龙","dog":u"犬","dog boy":u"男狗人","dog girl":u"犬娘","doll joints":u"球形关节","dolphin":u"海豚","donkey":u"毛驴","double anal":u"两屌一菊","double blowjob":u"两屌一口","double penetration":u"双穴贯通","double vaginal":u"两屌一屄","dougi":u"武道服","draenei":u"德莱尼","dragon":u"龙","drugs":u"沉浸药物","drunk":u"醉酒","dutch":u"荷兰语","ear fuck":u"耳交","eel":u"鳗鱼","eggs":u"产蛋","electric shocks":u"电击","elephant":u"大象","elf":u"小精灵","emotionless sex":u"无感情性交","enema":u"灌肠","english":u"英语","esperanto":u"世界语","estonian":u"爱沙尼亚语","exhibitionism":u"暴露狂","eye penetration":u"眼交","eyemask":u"眼部面具","eyepatch":u"眼罩","facesitting":u"颜面骑乘","fairy":u"妖精","farting":u"放屁","father":u"爸爸","females only":u"只有女性","femdom":u"女性主导","feminization":u"男变女","ffm threesome":u"两女一男","fft threesome":u"两女一扶她","figure":u"画像","filming":u"摄像","fingering":u"指奸","finnish":u"芬兰语","first person perspective":u"第一人称","fish":u"鱼","fisting":u"拳交","foot insertion":u"脚入屄","foot licking":u"舔足","footjob":u"足交","forbidden content":u"禁止的内容","forniphilia":u"人型家居","fox":u"狐狸","fox boy":u"男狐人","fox girl":u"狐娘","freckles":u"雀斑","french":u"法语","frog":u"青蛙","frottage":u"双屌互蹭","full body tattoo":u"全身纹身","full censorship":u"色块遮挡","full color":u"全彩","fundoshi":u"兜裆布","furry":u"人型兽","futanari":u"扶她","futanari on male":u"扶她X男人","gag":u"堵嘴","game sprite":u"像素画","gaping":u"豁开","garter belt":u"吊袜腰带","gasmask":u"防毒面具","gender bender":u"性别变化","german":u"德语","ghost":u"幽灵","giant":u"巨人","giantess":u"女巨人","gijinka":u"拟人化","glasses":u"眼镜","glory hole":u"墙上的孔","goat":u"山羊","goblin":u"地精","gokkun":u"饮精","gorilla":u"猩猩","gothic lolita":u"哥特洛丽塔","granddaughter":u"孙女","grandfather":u"爷爷","grandmother":u"奶奶","greek":u"希腊语","group":u"群P","growth":u"体型增大","guro":u"猎奇","gyaru":u"太妹","gyaru-oh\u200e":u"混混","gymshorts":u"拳击短裤","haigure":u"高叉马步","hairjob":u"发交","hairy":u"多阴毛","hairy armpits":u"腋下多毛","handicapped":u"残疾","handjob":u"套弄鸡鸡","hardcore":u"重口味","harem":u"后宫","harpy":u"鸟身女妖","hebrew":u"希伯来语","heterochromia":u"异色瞳","hijab":u"头巾","hindi":u"印地语","horse":u"马","horse boy":u"男马人","horse cock":u"马屌","horse girl":u"马娘","hotpants":u"热裤","how to":u"教程","huge breasts":u"超巨乳","huge penis":u"超大阴茎","human cattle":u"人型牲畜","human on furry":u"人与兽人","human pet":u"人型宠物","humiliation":u"凌辱","hungarian":u"匈牙利语","impregnation":u"内射","incest":u"乱伦","incomplete":u"不完整","indonesian":u"西澳特罗尼西亚语","infantilism":u"幼稚症","inflation":u"胀腹","insect":u"昆虫","insect boy":u"男昆虫人","insect girl":u"昆虫娘","inseki":u"姻亲","inverted nipples":u"凹陷乳头","invisible":u"隐身","italian":u"意大利语","japanese":u"日语","josou seme":u"女装攻","kangaroo":u"袋鼠","kappa":u"河童","kigurumi":u"玩偶服","kimono":u"和服","kindergarten uniform":u"幼儿园校服","kissing":u"接吻","kneepit sex":u"膝交","korean":u"韩语","kunoichi":u"女忍者","lab coat":u"白大褂","lactation":u"乳汁","large insertions":u"巨物插入","latex":u"乳胶衣","layer cake":u"换着插","leg lock":u"夹腿","legjob":u"腿交","leotard":u"连体衣","lingerie":u"内衣","lion":u"狮子","lioness":u"母狮","living clothes":u"触手服","lizard girl":u"蜥蜴娘","lizard guy":u"男蜥蜴人","lolicon":u"萝莉控","long tongue":u"长舌头","low bestiality":u"别标兽交","low lolicon":u"别标萝莉控","low shotacon":u"别标正太控","low toddlercon":u"别标婴儿控","machine":u"机械","maggot":u"蛆虫","magical girl":u"魔法少女","maid":u"女仆","malay":u"马来语","male on dickgirl":u"男人X扶她","males only":u"只有男性","masked face":u"戴面具","masturbation":u"手淫","mecha boy\u200e":u"机甲男","mecha girl":u"机甲娘","menstruation":u"经血","mermaid":u"美人鱼","merman":u"人鱼男","metal armor":u"金属盔甲","midget":u"侏儒","miko":u"日本巫女","milf":u"熟女","military":u"军装","milking":u"喷奶","mind break":u"精神崩溃","mind control":u"思想控制","minigirl":u"袖珍女人","miniguy":u"袖珍男人","minotaur":u"牛头人","missing cover":u"缺失封面","mmf threesome":u"两男一女","mmt threesome":u"两男一扶她","monkey":u"猴子","monoeye":u"天生独眼","monster":u"怪物","monster girl":u"怪物娘","moral degeneration":u"道德沦丧","mosaic censorship":u"马赛克遮挡","mother":u"妈妈","motorboating":u"埋胸","mouse":u"老鼠","mouse boy":u"男鼠人","mouse girl":u"鼠娘","mtf threesome":u"一男一女一扶她","multi-work series\u200e":u"卷作品","multiple arms":u"多个胳膊","multiple breasts":u"多个乳房","multiple nipples":u"多个乳头","multiple paizuri":u"多人乳交","multiple penises":u"多根阴茎","multiple vaginas":u"多条阴道","muscle":u"肌肉","muscle growth":u"肌肉增长","mute":u"哑巴","nakadashi":u"中出","navel fuck":u"肏肚脐","nazi":u"纳粹","necrophilia":u"奸尸","netorare":u"NTR爱人被睡","niece":u"侄女","ninja":u"忍者","nipple birth":u"乳头生育","nipple expansion":u"乳头膨大","nipple fuck":u"肏乳头","non-nude":u"非裸体","nose fuck":u"鼻交","nose hook":u"鼻钩","novel":u"小说","nun":u"修女","nurse":u"护士","octopus":u"章鱼","oil":u"抹油","old lady":u"老女人","old man":u"老男人","onahole":u"自慰器","oni":u"日本鬼","oppai loli":u"巨乳萝莉","orc":u"兽人","orgasm denial":u"禁止高潮","ostrich":u"鸵鸟","out of order":u"次序颠倒","oyakodon\u200e":u"母娘井","paizuri":u"乳交","panther":u"豹子","pantyhose":u"连裤袜","pantyjob":u"肏内裤","paperchild":u"纸孩","parasite":u"寄生","pasties":u"乳贴","pegging":u"女攻男受","penis birth":u"阴茎生育","petrification":u"石化","phimosis":u"包茎","phone sex":u"电话性爱","piercing":u"穿孔","pig":u"猪","pig girl":u"猪娘","pig man":u"男猪人","pillory":u"颈手枷","piss drinking":u"喝尿","plant girl":u"植物娘","pole dancing":u"钢管舞","policeman":u"男警察","policewoman":u"女警察","polish":u"波兰语","ponygirl":u"女骑师","poor grammar":u"语法错误","portuguese":u"葡萄牙语","possession":u"占据","pregnant":u"孕妇","prehensile hair":u"抓着头发","prolapse":u"脱垂","prostate massage":u"前列腺按摩","prostitution":u"卖淫","pubic stubble":u"阴毛茬","public use":u"公共使用","rabbit":u"兔子","raccoon boy":u"浣熊男孩","raccoon girl\u200e":u"浣熊娘","race queen":u"赛车女郎","randoseru":u"日式小学书包","rape":u"强奸","realporn":u"真正的色情","redraw":u"重绘","replaced":u"已更换","reptile":u"爬行","rewrite":u"重改标签","rhinoceros":u"犀牛","rimjob":u"舔菊","robot":u"机器人","robot girl":u"机器娘","romanian":u"罗马尼亚语","russian":u"俄罗斯语","ryona":u"虐女萌","saliva":u"唾液","sample":u"样本","scanmark":u"扫描","scar":u"伤疤","scat":u"排粪","school swimsuit":u"学校泳装","schoolboy":u"男学生","schoolboy uniform":u"男学生校服","schoolgirl":u"女学生","schoolgirl uniform":u"女学生校服","screenshots":u"截图","scrotal lingerie":u"阴囊内衣","selfcest":u"自己X自己","sex toys":u"性玩具","shared senses":u"感官共享","shark":u"鲨鱼","shark boy":u"鲨鱼男","shark girl":u"鲨鱼娘","sheep":u"羊","sheep boy":u"绵羊男","sheep girl":u"绵羊娘","shemale":u"人妖","shibari":u"绳艺","shimapan":u"条纹内裤","shotacon":u"正太控","shrinking":u"体型缩小","sister":u"姐/妹","skinsuit":u"人皮衣","slave":u"奴隶","sleeping":u"睡奸","slime":u"史莱姆","slime boy\u200e":u"史莱姆男","slime girl":u"史莱姆娘","slovak":u"斯洛伐克语","slug":u"蛞蝓","small breasts":u"贫乳","smegma":u"包皮垢","smell":u"闻味道","smoking":u"性交吸烟","snake":u"蛇","snake boy":u"蛇男","snake girl":u"蛇女","snuff":u"虐杀","sole dickgirl":u"单扶她","sole female":u"单女","sole male":u"单男","solo action":u"自慰","spanish":u"西班牙语","spanking":u"打屁股","speculum":u"内窥器","speechless":u"无文字","spider":u"蜘蛛","spider girl":u"蜘蛛娘","squid girl":u"鱿鱼娘","squirting":u"潮吹","stereoscopic":u"可用立体眼镜","stewardess":u"制服","stockings":u"丝袜","stomach deformation":u"胃变形","story arc":u"故事框架","strap-on":u"假阳具","stretching":u"扩张","stuck in wall":u"卡墙里","sumata":u"股间性交","sundress":u"背心裙","sunglasses":u"太阳镜","sweating":u"出汗","swedish":u"瑞典语","swimsuit":u"泳装","swinging":u"夫妇招人","syringe":u"注射器","table masturbation":u"桌子自慰","tagalog":u"他加禄语","tail plug":u"肛塞","tailjob":u"尾交","tall girl":u"高个女","tall man":u"高个男","tankoubon":u"单行本","tanlines":u"日晒线","teacher":u"教师","tentacles":u"触手","text cleaned":u"无嵌字版","thai":u"泰语","themeless":u"没有主题","thigh high boots":u"过膝长靴","tiara":u"冠状头饰","tickling":u"瘙痒","tiger":u"老虎","tights":u"紧身服","time stop":u"时间停止","toddlercon":u"婴儿控","tomboy":u"假小子","tomgirl":u"伪娘","tooth brushing":u"刷牙调情","torture":u"酷刑","tracksuit":u"运动服","trampling":u"踩踏","transformation":u"身体变化","translated":u"译制品","tribadism":u"两屄互蹭","triple anal":u"三屌一菊花","triple penetration":u"三穴贯通","triple vaginal":u"三屌一屄","ttf threesome":u"两扶她一女","ttm threesome":u"两扶她一男","tube":u"插管","turkish":u"乌克兰语","turtle":u"乌龟","tutor":u"家教","twins":u"双胞胎","ukrainian":u"乌克兰语","unbirth":u"钻进屄里","uncensored":u"无修正","uncle":u"叔舅","underwater":u"水下性爱","unicorn":u"独角兽","unusual pupils":u"非正常瞳孔","unusual teeth":u"特殊牙齿","urethra insertion":u"尿道插入","urination":u"放尿","vacbed":u"乳胶真空床","vaginal sticker":u"小穴贴","vampire":u"吸血鬼","vietnamese":u"越南语","virginity":u"处女","vomit":u"呕吐","vore":u"捕食","voyeurism":u"偷窥","waiter":u"男服务员","waitress":u"女服务员","watermarked":u"有水印","webtoon":u"网页多媒体漫画","weight gain":u"体重增加","wet clothes":u"湿身","whale":u"鲸鱼","whip":u"鞭打","widow":u"寡妇","widower":u"鳏夫","wings":u"翅膀","witch":u"美式女巫","wolf":u"狼","wolf boy":u"男狼人","wolf girl":u"狼女","wooden horse":u"木马","worm":u"虫子","wormhole":u"虫洞","wrestling":u"摔跤","x-ray":u"透视","yandere":u"病娇","yaoi":u"男同","yukkuri":u"油库里","yuri":u"女同","zebra":u"斑马","zombie":u"丧尸"}
    regex = re.compile("[(female)(male)]\s?:\s?(.*)")
    shadow = list(tags)
    for origin_t in tags:
        result = regex.findall(origin_t.lower())
        key = result[0] if len(result) > 0 else origin_t.lower()
        if origin_t.startswith("artist"):
            shadow.remove(origin_t)
        if key in zh_json:
            shadow.remove(origin_t)
            shadow.append(zh_json[key])
    return shadow

class Ehentai(Source):
    
    name = 'E-hentai Galleries'
    author = 'Wu yuan'
    version = (1,1,3)
    minimum_calibre_version = (2, 80, 0)
    
    description = _('Download metadata and cover from e-hentai.org.'
                   'Useful only for doujinshi.')
    
    capabilities = frozenset(['identify', 'cover'])
    touched_fields = frozenset(['title','authors','tags','rating','publisher','identifier:ehentai'])
    supports_gzip_transfer_encoding = True
    cached_cover_url_is_reliable = True
    
    EHentai_url = 'https://e-hentai.org/g/%s/%s/'
    ExHentai_url = 'https://exhentai.org/g/%s/%s/'
    
    options = (
        Option('Use_Exhentai','bool',False,_('Use Exhentai'),
               _('If Use Exhentai is True, the plugin will search metadata on exhentai.')),
        Option('ipb_member_id','string',None,_('ipb_member_id'),
               _('If Use Exhentai is True, please input your cookies.')),
        Option('ipb_pass_hash','string',None,_('ipb_pass_hash'),
               _('If Use Exhentai is True, please input your cookies.')),
        Option('translate_tag','bool',False,_('translate_tag'),
               _('If wanna get a translated tag, check this'))
               )
    
    config_help_message = ('<p>'+_('To Download Metadata from exhentai.org you must sign up'
                            ' a free account and get the cookies of .exhentai.org.'
                            ' If you don\'t have an account, you can <a href="%s">sign up</a>.')) % 'https://forums.e-hentai.org/index.php'
    
    def __init__(self, *args, **kwargs): # {{{
        Source.__init__(self, *args, **kwargs)
        self.config_exhentai()
    # }}}

    def config_exhentai(self): # {{{
        
        ExHentai_Status = self.prefs['Use_Exhentai']
        ExHentai_Cookies = [{'name':'ipb_member_id', 'value':self.prefs['ipb_member_id'], 'domain':'.exhentai.org', 'path':'/'},
                            {'name':'ipb_pass_hash', 'value':self.prefs['ipb_pass_hash'], 'domain':'.exhentai.org', 'path':'/'}]
        
        if ExHentai_Status is True:
            for cookie in ExHentai_Cookies:
                if cookie['value'] is None:
                    ExHentai_Status = False
                    break
        
        self.ExHentai_Status = ExHentai_Status
        self.ExHentai_Cookies = ExHentai_Cookies
        return
    # }}}
    
    def create_query(self,log,title=None, authors=None,identifiers={},is_exhentai=False): # {{{
                
        EHentai_SEARCH_URL = 'https://e-hentai.org/?'
        ExHentai_SEARCH_URL = 'https://exhentai.org/?'
        
        q = ''
        
        if title or authors:
            def build_term(type,parts):
                return ' '.join(x for x in parts)
            title_token = list(self.get_title_tokens(title))
            if title_token:
                q = q + build_term('title',title_token)
            author_token = list(self.get_author_tokens(authors, only_first_author=True))
            if author_token:
                q = q + (' ' if q != '' else '') + build_term('author', author_token)
        q = q.strip()
        if isinstance(q, unicode):
            q = q.encode('utf-8')
        if not q:
            return None
        q_dict = {'f_doujinshi':1, 'f_manga':1, 'f_artistcg':1, 'f_gamecg':1, 'f_western':1, 'f_non-h':1,
                  'f_imageset':1, 'f_cosplay':1, 'f_asianporn':1, 'f_misc':1, 'f_search':q, 'f_apply':'Apply+Filter',
                  'advsearch':1, 'f_sname':'on', 'f_sh':'on', 'f_srdd':2}
        if is_exhentai is False:
            url = EHentai_SEARCH_URL + urlencode(q_dict)
        else:
            url = ExHentai_SEARCH_URL + urlencode(q_dict)
        return url
    # }}}
    
    def get_gallery_info(self,log,raw): # {{{
        
        pattern = re.compile(r'https:\/\/(?:e-hentai\.org|exhentai\.org)\/g\/(?P<gallery_id>\d+)/(?P<gallery_token>\w+)/')
        results = re.findall(pattern,raw)
        if not results:
            log.exception('Failed to get gallery_id and gallery_token!')
            return None
        gidlist = []
        for r in results:
            gidlist.append(list(r))
        return gidlist
    # }}}
    
    def get_all_details(self,gidlist,log,abort,result_queue,timeout): # {{{
        
        EHentai_API_url = 'https://api.e-hentai.org/api.php'
        br = self.browser
        data = {"method": "gdata","gidlist": gidlist,"namespace": 1}
        data = json.dumps(data)
        try:
            raw = br.open_novisit(EHentai_API_url,data=data,timeout=timeout).read()
        except Exception as e:
            log.exception('Failed to make api request.',e)
            return
        gmetadatas = json.loads(raw)['gmetadata']
        for relevance, gmetadata in enumerate(gmetadatas):
            try:
                ans = to_metadata(log, gmetadata,self.ExHentai_Status, self.prefs['translate_tag'])
                if isinstance(ans, Metadata):
                    ans.source_relevance = relevance
                    db = ans.identifiers['ehentai']
                    if ans.has_ehentai_cover:
                        self.cache_identifier_to_cover_url(db,ans.has_ehentai_cover)
                    self.clean_downloaded_metadata(ans)
                    result_queue.put(ans)
            except:
                log.exception('Failed to get metadata for identify entry:',gmetadata)
            if abort.is_set():
                break
    # }}}
    
    def get_book_url(self, identifiers): # {{{
        
        db = identifiers.get('ehentai',None)
        d = {'0':False,'1':True}
        if db is not None:
            gid,token,s = re.split('_', db)
            ExHentai_Status = d[str(s)]
            if ExHentai_Status:
                url = self.ExHentai_url % (gid,token)
            else:
                url = self.EHentai_url % (gid,token)
            return ('ehentai', db, url)
    # }}}

    def download_cover(self, log, result_queue, abort,title=None, authors=None, identifiers={}, timeout=30, get_best_cover=False): # {{{

        cached_url = self.get_cached_cover_url(identifiers)
        if cached_url is None:
            return
        if abort.is_set():
            return
        br = self.browser
        log('Downloading cover from:', cached_url)
        try:
            cdata = br.open_novisit(cached_url, timeout=timeout).read()
            if cdata:
                result_queue.put((self, cdata))
        except:
            log.exception('Failed to download cover from:', cached_url)
    # }}}

    def get_cached_cover_url(self, identifiers): # {{{
        
        url = None
        db = identifiers.get('ehentai',None)
        if db is None:
            pass
        if db is not None:
            url = self.cached_identifier_to_cover_url(db)
        return url
    # }}}

    def identify(self, log, result_queue, abort, title=None, authors=None,identifiers={}, timeout=30): # {{{
        
        is_exhentai = self.ExHentai_Status
        query = self.create_query(log,title=title, authors=authors,identifiers=identifiers,is_exhentai=is_exhentai)
        if not query:
            log.error('Insufficient metadata to construct query')
            return
        br = self.browser
        if is_exhentai is True:
            for cookie in self.ExHentai_Cookies:
                br.set_cookie(name=cookie['name'], value=cookie['value'], domain=cookie['domain'], path=cookie['path'])
        try:
            _raw = br.open_novisit(query,timeout=timeout)
            raw = _raw.read()
        except Exception as e:
            log.exception('Failed to make identify query: %r'%query)
            return as_unicode(e)
        if not raw and identifiers and title and authors and not abort.is_set():
            return self.identify(log, result_queue, abort, title=title,authors=authors, timeout=timeout)
        if is_exhentai is True: 
            try:
                'https://exhentai.org/' in raw
            except Exception as e:
                log.error('The cookies for ExHentai is invalid.')
                log.error('Exhentai cookies:')
                log.error(self.ExHentai_Cookies)
                return
        gidlist = self.get_gallery_info(log,raw)
        if not gidlist:
            log.error('No result found.\n','query: %s' % query)
            return
        self.get_all_details(gidlist=gidlist, log=log, abort=abort, result_queue=result_queue, timeout=timeout)
    # }}}
        
if __name__ == '__main__': # tests {{{
    # To run these test use: calibre-customize -b ehentai_metadata && calibre-debug -e ehentai_metadata/__init__.py
    from calibre.ebooks.metadata.sources.test import (test_identify_plugin,
        title_test, authors_test)

    test_identify_plugin(Ehentai.name,
        [
            (
                {'title': 'キリト君の白くべたつくなにか', 'authors':['しらたま肉球']},
                [title_test('キリト君の白くべたつくなにか', exact=False)]
            ),
            (
                {'title':'拘束する部活動 (僕は友達が少ない)','authors':['すもも堂 (すももEX) ','有条色狼']},
                [title_test('拘束する部活動', exact=False)]
            ),
            (
                {'title':'桜の蜜','authors':['劇毒少女 (ke-ta)']},
                [title_test('桜の蜜', exact=False)]
            )
    ])
# }}}
