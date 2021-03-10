# Django
from django.utils.timezone import now

# Django REST framework
from rest_framework import serializers

# Self
from ..models import Event, Record


def time_diff(time_start, time_end):
    result = time_end - time_start
    hours = int(result.seconds / 3600)
    minutes = int(result.seconds % 3600 / 60)
    seconds = result.seconds % 3600 % 60

    text = ''
    if result.days > 0:
        text += "{0}天 ".format(result.days)
    if hours > 0:
        text += "{0}时 ".format(hours)
    if minutes > 0:
        text += "{0}分 ".format(minutes)

    text += "{0}秒".format(seconds)
    return text


class RecordModifySerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    state_display = serializers.CharField(source='get_state_display', read_only=True, required=False)

    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = ['created', 'modified', 'created_by', 'modified_by', 'state_display']

    def validate_state(self, state):
        instance_record = Record.objects.filter(event_id=self.context['request'].data.get('event'), state=state)
        if int(state) in [0, 6] and len(instance_record) > 0:
            raise serializers.ValidationError('状态已存在')
        return state

    def create(self, validated_data):
        # 新建预定义数据
        if validated_data.get('state_display'):
            del validated_data['state_display']
        instance = super(RecordModifySerializer, self).create(validated_data)
        # 更新事件的状态
        instance_event = Event.objects.filter(pk=validated_data['event'].id).first()
        if instance_event:
            instance_event.current_state = validated_data['state']
            instance_event.save()
        return instance

    def update(self, instance, validated_data):
        if validated_data.get('state_display'):
            del validated_data['state_display']
        instance_record = super(RecordModifySerializer, self).update(instance, validated_data)
        # 更新事件的状态
        instance_event = Event.objects.filter(pk=validated_data['event'].id).first()
        if instance_event:
            instance_event.current_state = validated_data['state']
            instance_event.save()

        return instance_record


class RecordListSerializer(serializers.ModelSerializer):
    """
    记录列表的序列化
    """

    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    state_display = serializers.CharField(source='get_state_display', read_only=True, required=False)

    class Meta:
        model = Record
        fields = ['id', 'title', 'state', 'current_operator', 'description', 'created_by', 'modified_by', 'created',
                  'modified', 'state_display']
        read_only_fields = ['created', 'modified', 'created_by', 'modified_by']


class EventListSerializer(serializers.ModelSerializer):
    """
    事件列表的序列化
    """
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    level_display = serializers.CharField(source='get_level_display', read_only=True, required=False)
    current_state_display = serializers.CharField(source='get_current_state_display', read_only=True, required=False)

    class Meta:
        model = Event
        fields = ['id', 'sn', 'name', 'level', 'level_display', 'current_state', 'current_state_display',
                  'current_operator', 'related_resources', 'description',
                  'occurrence_date', 'created_by', 'modified_by', 'created', 'modified']
        read_only_fields = ['sn', 'created', 'modified', 'created_by', 'modified_by']
        depth = 1


class EventModifySerializer(serializers.ModelSerializer):
    """
    事件列表的序列化
    """
    records = serializers.SerializerMethodField()
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    level_display = serializers.CharField(source='get_level_display', read_only=True, required=False)
    current_state_display = serializers.CharField(source='get_current_state_display', read_only=True, required=False)
    mttr = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = Event
        fields = ['id', 'sn', 'name', 'level', 'level_display', 'current_state', 'current_state_display',
                  'current_operator', 'related_resources', 'description',
                  'occurrence_date', 'created_by', 'modified_by', 'created', 'modified', 'records', 'mttr']
        read_only_fields = ['sn', 'created', 'modified', 'created_by', 'modified_by']
        depth = 1

    def get_records(self, obj):
        record_obj = Record.objects.filter(event=obj).order_by('-created')
        serializer = RecordListSerializer(record_obj, many=True)
        return serializer.data

    def get_mttr(self, obj):
        record_obj = Record.objects.filter(event=obj).order_by('-created')

        mtti = self.instance.occurrence_date
        mttk_end = mttf_end = mttv_start = mttv_end = ''
        data = {
            'mtti': mtti.strftime("%Y-%m-%d %H:%M:%S"),
            'mttk': '',
            'mttf': '',
            'mttv': ''
        }

        for i in record_obj:
            if i.state == 3:
                mttk_end = i.created
            elif i.state == 2:
                mttf_end = i.created
            elif i.state == 5:
                mttv_start = i.created
            elif i.state == 6:
                mttv_end = i.created

        if mttk_end:
            data['mttk'] = "{start} - {end}  持续时间: {desc}".format(start=mtti.strftime("%Y-%m-%d %H:%M:%S"),
                                                                  end=mttk_end.strftime("%Y-%m-%d %H:%M:%S"),
                                                                  desc=time_diff(mtti, mttk_end))
        else:
            data['mttk'] = "{start} - ".format(start=mtti.strftime("%Y-%m-%d %H:%M:%S"))
        if mttf_end:
            data['mttf'] = "{start} - {end}  持续时间: {desc}".format(start=mtti.strftime("%Y-%m-%d %H:%M:%S"),
                                                                  end=mttf_end.strftime("%Y-%m-%d %H:%M:%S"),
                                                                  desc=time_diff(mtti, mttf_end))
        else:
            data['mttf'] = "{start} - ".format(start=mtti.strftime("%Y-%m-%d %H:%M:%S"))
        if mttv_start:
            if mttv_end:
                data['mttv'] = "{start} - {end}  持续时间: {desc}".format(start=mttv_start.strftime("%Y-%m-%d %H:%M:%S"),
                                                                      end=mttv_end.strftime("%Y-%m-%d %H:%M:%S"),
                                                                      desc=time_diff(mttv_start, mttv_end))
            else:
                data['mttv'] = "{start} - ".format(start=mttv_start.strftime("%Y-%m-%d %H:%M:%S"))

        return data

    def create(self, validated_data):
        # 新建预定义数据
        if 'sn' not in validated_data:
            validated_data['sn'] = 'SJ' + now().strftime('%Y%m%d%H%M%S')
            validated_data['current_state'] = 0

        if validated_data.get('level_display'):
            del validated_data['level_display']
        if validated_data.get('current_state_display'):
            del validated_data['current_state_display']

        instance = super(EventModifySerializer, self).create(validated_data)
        # 新建第一条记录
        instance_record = Record(event=instance, title="事件新建", state=0, current_operator='系统创建', description="第一条事件记录！")
        instance_record.save()
        return instance

    def update(self, instance, validated_data):
        if validated_data.get('level_display'):
            del validated_data['level_display']
        if validated_data.get('current_state_display'):
            del validated_data['current_state_display']

        instance_event = super(EventModifySerializer, self).update(instance, validated_data)
        if validated_data.get('current_state') == 6:
            # 新建最后第一条记录
            instance_record = Record.objects.get_or_create(event=instance, title="事件结束", state=6, current_operator='系统创建',
                                                           description="此事件已结束！")
        return instance_event
