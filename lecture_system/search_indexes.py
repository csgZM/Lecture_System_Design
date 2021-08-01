#定义索引类
from haystack import indexes
# 导入模型类
from lecture_system.models import Lecture_Message
#索引建立的命令python manage.py rebuild_index
#更新索引的命令 python manage.py update_index
#指定对于某个类的某些数据建立索引
class Lecture_MessageIndex(indexes.SearchIndex, indexes.Indexable):
    # 索引字段
    # use_template=True指定根据表中的那些字段建立索引文件，把说明放在一个文件中
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        # 返回你的模型类
        return Lecture_Message

    # 建立索引的数据
    def index_queryset(self, using=None):
        return self.get_model().objects.all()