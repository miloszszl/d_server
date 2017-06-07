from rest_framework import serializers
from .models import User,Test,Page,Page_Test,Page_Connection,T_P_B,Button,Page_Host,Batch
from django.db.models import Max,Min,Sum
import copy
from datetime import datetime, timedelta
from django.db.models import Q
import hashlib

class SecretSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=64)   #hashlib.sha224(b"Nobody inspects the spammish repetition").hexdigest()


class Page_HostSerializer(serializers.ModelSerializer):

    class Meta:
        model=Page_Host
        fields=('domain_name','ipv4')


class PageAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Page
        fields=('address',)


class Page_ConnectionSerializer(serializers.ModelSerializer):
    page_2 = PageAddressSerializer(required=False,allow_null=True)

    class Meta:
        model=Page_Connection
        fields=('page_2',)


class T_P_BSerializer(serializers.ModelSerializer):
    class Meta:
        model=T_P_B
        fields=('is_working',)


class ButtonSerializer(serializers.ModelSerializer):
    t_p_b=T_P_BSerializer(source='t_p_b_b',many=True,required=False,allow_null=True)

    class Meta:
        model=Button
        fields=('locator','t_p_b',)

class PageSerializer(serializers.ModelSerializer):
    page_connections=Page_ConnectionSerializer(source='page_connection_1',many=True,required=False,allow_null=True)
    buttons=ButtonSerializer(source='button_p',many=True,required=False,allow_null=True)
    host=Page_HostSerializer(required=False,allow_null=True)

    class Meta:
        model=Page
        fields=('address','weight','encoding','cookies_present', 'force_test','weight_w_pictures','host','page_connections','buttons')


class Page_TestSerializer(serializers.ModelSerializer):
    page=PageSerializer(required=False,allow_null=True)
    # redirection=PageSerializer(required=False,allow_null=True)
    redirection = PageAddressSerializer(required=False, allow_null=True)

    class Meta:
        model=Page_Test
        fields=('is_working','response_code','download_time','page','redirection')


class BatchSerializer(serializers.ModelSerializer):
    page_address=PageAddressSerializer(source='page')

    class Meta:
        model=Batch
        fields=('levels','page_address',)


class TestSerializer(serializers.ModelSerializer):
    pages_tests=Page_TestSerializer(source='page_test_t',many=True,required=False,allow_null=True)
    batch=BatchSerializer(source='batch_t',many=True,required=False,allow_null=True)

    class Meta:
        model=Test
        fields=('date','batch','pages_tests')


class UserSerializer(serializers.ModelSerializer):
    tests=TestSerializer(source='test_u',many=True,required=False,allow_null=True)
    secret =SecretSerializer(allow_null=True,required=False,)

    class Meta:
        model=User
        fields=('secret','ipv4', 'transfer_speed', 'mac_address', 'tests',)

    def create(self, validated_data):
        tests_list = validated_data.pop('tests', None)
        secret=validated_data.pop('secret',None)
        if secret is None:
            return None
        else:
            key_from_user=secret.get('key',None)
            if key_from_user is None:
                return None
            else:
                mac_address = validated_data.get('mac_address', None)
                ipv4 = validated_data.get('ipv4', None)
                if mac_address is None or ipv4 is None:
                    return None
                else:
                    secret_key=mac_address+"trochegruzu*74"+ipv4+"posolecietroche@11"
                    my_bytes = bytes(secret_key, encoding='utf-8')
                    code = hashlib.sha256(my_bytes).hexdigest()
                    if code != key_from_user:
                        return None

        user = User.objects.filter(mac_address=validated_data.get('mac_address',None), ipv4=validated_data.get('ipv4',None),
                                transfer_speed=validated_data.get('transfer_speed',None))
        #user
        if len(user)<=0:
            user = User.objects.create(**validated_data)
        else:
            user=user[0]
        #tests
        if tests_list is not None:
            for test in tests_list:
                if test is not None:
                    batches_list = test.pop('batch', None)
                    pages_tests_list = test.pop('pages_tests', None)
                    t_obj = Test.objects.create(user=user, **test)

                    if pages_tests_list is not None:
                        for pt_data in pages_tests_list:
                            if pt_data is not None:
                                page_data=pt_data.pop('page', None)
                                redirection_data=pt_data.pop('redirection', None)

                                pt_obj = Page_Test.objects.create(test=t_obj, redirection=None, **pt_data)
                                if page_data is not None and page_data.get('domain_name',None) is not None and\
                                        page_data.get('domain_name',None)!="":
                                    host_data=page_data.pop('host', None)

                                    ph_obj=None

                                    if host_data is not None and host_data.get('domain_name',None) is not None and\
                                        host_data.get('domain_name',None)!="":
                                        ph_obj=Page_Host.objects.filter(domain_name=host_data.get('domain_name',None))#, ipv4=host_data.get('ipv4',None)

                                        if len(ph_obj) <= 0:
                                            ph_obj=Page_Host.objects.create(**host_data)
                                        else:
                                            ph_obj=ph_obj[0]

                                    page_connections_list=page_data.pop('page_connections', None)
                                    buttons_list=page_data.pop('buttons', None)
                                    p_obj=Page.objects.filter(address=page_data.get('address',None))
                                    if len(p_obj)<=0:
                                        p_obj=Page.objects.create(host=ph_obj,**page_data)
                                    else:
                                        p_obj=p_obj[0]
                                        val = page_data.get('weight', None)
                                        if val!=None:
                                            p_obj.weight=val

                                        val = page_data.get('encoding', None)
                                        if val != None:
                                            p_obj.encoding=val

                                        val = page_data.get('weight_w_pictures', None)
                                        if val != None:
                                            p_obj.weight_w_pictures=val

                                        val = page_data.get('cookies_present', None)
                                        if val != None:
                                            p_obj.cookies_present=val

                                        val = page_data.get('force_test', None)
                                        if val != None:
                                            p_obj.force_test=page_data['force_test']

                                        p_obj.save()

                                    pt_obj.page=p_obj
                                    if pt_obj.download_time == 0:
                                        pt_obj.download_time=None;
                                    pt_obj.save()

                                    #global_working_percentage
                                    total_pt1=Page_Test.objects.filter(~Q(is_working=None),page=p_obj).count()
                                    global_working_percentage_pt=None
                                    if total_pt1 > 0:
                                        working_pt1=Page_Test.objects.filter(page=p_obj,is_working=True).count()
                                        global_working_percentage_pt=working_pt1/total_pt1*100.0

                                    #local working percentage
                                    d = datetime.today() - timedelta(days=30)
                                    tests_local=Test.objects.filter(date__gte=d)
                                    total_pt2 = Page_Test.objects.filter(page=p_obj,test__in=tests_local).count()
                                    last_month_working_percentage_pt=None
                                    if total_pt2>0:
                                        working_pt2 = Page_Test.objects.filter(page=p_obj,test__in=tests_local,is_working=True).count()
                                        last_month_working_percentage_pt=working_pt2/total_pt2*100.0

                                    #redirection percentage
                                    not_null_redir = Page_Test.objects.filter(~Q(redirection=None),page=p_obj).count()
                                    total_pt3=Page_Test.objects.filter(page=p_obj).count()
                                    redir_percentage = None
                                    if total_pt3>0:
                                        redir_percentage=not_null_redir/total_pt3*100.0

                                    #avg_download time
                                    time_sum=Page_Test.objects.filter(page=p_obj,download_time__gte=0).aggregate(time=Sum('download_time'))
                                    pt_count=Page_Test.objects.filter(page=p_obj,download_time__gte=0).count()
                                    avg_download_time=None
                                    if time_sum.get('time',None) is not None and len(time_sum)>0 and pt_count>0:
                                        avg_download_time=time_sum.get('time',None)/pt_count

                                    p_obj.last_month_working_percentage=last_month_working_percentage_pt
                                    p_obj.global_working_percentage=global_working_percentage_pt
                                    p_obj.redirection_percentage=redir_percentage
                                    p_obj.avg_download_time=avg_download_time
                                    p_obj.save()

                                    if page_connections_list is not None:
                                        for pc in page_connections_list:
                                            if pc is not None:
                                                page_2=pc['page_2']
                                                page_for_pc=Page.objects.filter(address=page_2['address'])
                                                if page_for_pc is not None and len(page_for_pc)>0:
                                                    page_2_for_pc=page_for_pc[0]
                                                    Page_Connection.objects.create(page_1=p_obj,page_2=page_2_for_pc)
                                                else:
                                                    page_2_for_pc = Page.objects.create(address=page_2['address'])
                                                    Page_Connection.objects.create(page_1=p_obj, page_2=page_2_for_pc)

                                    #buttons
                                    if buttons_list is not None:
                                        for button in buttons_list:
                                            if button is not None:
                                                t_p_b_list=button.pop('t_p_b', None)
                                                b=Button.objects.filter(locator=button['locator'],page=p_obj)
                                                if b is None or len(b) <= 0:
                                                    b = Button.objects.create(page=p_obj, **button)
                                                else:
                                                    b=b[0]

                                                for t_p_b in t_p_b_list:
                                                    if t_p_b is not None:
                                                        T_P_B.objects.create(button=b, page_test=pt_obj, is_working=t_p_b['is_working'])

                                                # global_working_percentage
                                                total_tpb1 = T_P_B.objects.filter(button=b).count()
                                                global_working_percentage_tpb = None
                                                if total_tpb1 > 0:
                                                    working_tpb1 = T_P_B.objects.filter(button=b,
                                                                                           is_working=True).count()
                                                    global_working_percentage_tpb = working_tpb1 / total_tpb1 * 100.0

                                                # local working percentage
                                                d2 = datetime.today() - timedelta(days=30)
                                                tl = Test.objects.filter(date__gte=d2)
                                                pt = Page_Test.objects.filter(page=p_obj,test__in=tl)
                                                total_tpb2=T_P_B.objects.filter(button=b,page_test__in=pt).count()
                                                last_month_working_percentage_tpb = None
                                                if total_tpb2 > 0:
                                                    working_tpb2 = T_P_B.objects.filter(button=b, page_test__in=pt,
                                                                                        is_working=True).count()
                                                    last_month_working_percentage_tpb = working_tpb2 / total_tpb2 * 100.0

                                                    b.last_month_working_percentage = last_month_working_percentage_tpb
                                                    b.global_working_percentage = global_working_percentage_tpb
                                                    b.save()

                                if redirection_data is not None:
                                    address=redirection_data.get('address',None)
                                    if address is not None:
                                        page = Page.objects.filter(address=address)
                                        if len(page)>0:
                                            page=page[0]
                                        else:
                                            page=Page.objects.create(address=address)

                                        pt_obj.redirection=page
                                        pt_obj.save()


                                    # host_data = redirection_data.pop('host', None)
                                    #
                                    # ph_obj=None
                                    # if host_data is not None:
                                    #     ph_obj = Page_Host.objects.filter(domain_name=host_data['domain_name'],
                                    #                                   ipv4=host_data['ipv4'])
                                    #     if len(ph_obj) <= 0 :
                                    #         ph_obj = Page_Host.objects.create(**host_data)
                                    #     else:
                                    #         ph_obj = ph_obj[0]
                                    #
                                    # page_connections_list = redirection_data.pop('page_connections', None)
                                    # buttons_list = redirection_data.pop('buttons', None)
                                    #
                                    # p_obj = Page.objects.filter(address=redirection_data.get('address',None))
                                    # if len(p_obj) <= 0:
                                    #     p_obj = Page.objects.create(host=ph_obj, **redirection_data)
                                    # else:
                                    #     p_obj = p_obj[0]
                                    #     val = redirection_data.get('weight', None)
                                    #     if val != None:
                                    #         p_obj.weight = val
                                    #
                                    #     val = redirection_data.get('encoding', None)
                                    #     if val != None:
                                    #         p_obj.encoding = val
                                    #
                                    #     val = redirection_data.get('weight_w_pictures', None)
                                    #     if val != None:
                                    #         p_obj.weight_w_pictures = val
                                    #
                                    #     val = redirection_data.get('cookies_present', None)
                                    #     if val != None:
                                    #         p_obj.cookies_present = val
                                    #
                                    #     val = redirection_data.get('force_test', None)
                                    #     if val != None:
                                    #         p_obj.force_test = redirection_data['force_test']
                                    #     p_obj.save()
                                    #
                                    # if pt_obj is not None:
                                    #     pt_obj.redirection=p_obj
                                    #     pt_obj.save()
                                    #
                                    # # global_working_percentage
                                    # total_pt1 = Page_Test.objects.filter(Q(page=p_obj) | Q(redirection=p_obj)).count()
                                    # global_working_percentage_pt = None
                                    # if total_pt1 > 0:
                                    #     working_pt1 = Page_Test.objects.filter(Q(Q(page=p_obj) | Q(redirection=p_obj)),
                                    #                                            is_working=True).count()
                                    #     global_working_percentage_pt = working_pt1 / total_pt1 * 100.0
                                    #
                                    # # local working percentage
                                    # d = datetime.today() - timedelta(days=30)
                                    # tests_local = Test.objects.filter(date__gte=d)
                                    # total_pt2 = Page_Test.objects.filter(Q(Q(page=p_obj) | Q(redirection=p_obj)), test__in=tests_local).count()
                                    # last_month_working_percentage_pt = None
                                    # if total_pt2 > 0:
                                    #     working_pt2 = Page_Test.objects.filter(Q(Q(page=p_obj) | Q(redirection=p_obj)),
                                    #                                            test__in=tests_local,is_working=True).count()
                                    #     last_month_working_percentage_pt = working_pt2 / total_pt2 * 100.0
                                    #
                                    # # redirection percentage
                                    # not_null_redir = Page_Test.objects.filter(~Q(redirection=None),
                                    #                                           Q(Q(page=p_obj) | Q(redirection=p_obj))).count()
                                    # redir_percentage=None
                                    # if total_pt1>0:
                                    #     redir_percentage=not_null_redir/total_pt1*100.0
                                    #
                                    # # avg_download time
                                    # time_sum = Page_Test.objects.filter(Q(Q(page=p_obj) | Q(redirection=p_obj)),
                                    #                                     download_time__gte=0).aggregate(
                                    #                                     time=Sum('download_time'))
                                    # avg_download_time=None
                                    # if time_sum.get('time',None) is not None and len(time_sum)>0:
                                    #     avg_download_time = time_sum.get('time',None) / total_pt1
                                    #
                                    # p_obj.last_month_working_percentage = last_month_working_percentage_pt
                                    # p_obj.global_working_percentage = global_working_percentage_pt
                                    # p_obj.redirection_percentage = redir_percentage
                                    # p_obj.avg_download_time = avg_download_time
                                    # p_obj.save()
                                    #
                                    # if page_connections_list is not None:
                                    #     for pc in page_connections_list:
                                    #         if pc is not None:
                                    #             page_2 = pc.get('page_2',None)
                                    #             if page_2 is not None:
                                    #                 page_for_pc = Page.objects.filter(address=page_2.get('address',None))
                                    #                 if len(page_for_pc) > 0:
                                    #                     page_2_for_pc = page_for_pc[0]
                                    #                     Page_Connection.objects.create(page_1=p_obj, page_2=page_2_for_pc)
                                    #                 else:
                                    #                     page_2_for_pc = Page.objects.create(address=page_2.get('address',None))
                                    #                     Page_Connection.objects.create(page_1=p_obj, page_2=page_2_for_pc)
                                    #
                                    # # buttons
                                    # if buttons_list is not None:
                                    #     for button in buttons_list:
                                    #         if button is not None:
                                    #             t_p_b_list = button.pop('t_p_b', None)
                                    #             b = Button.objects.filter(locator=button.get('locator',None), page=p_obj)
                                    #             if len(b) <= 0:
                                    #                 b = Button.objects.create(page=p_obj, **button)
                                    #             else:
                                    #                 b = b[0]
                                    #
                                    #             for t_p_b in t_p_b_list:
                                    #                 if t_p_b is not None:
                                    #                     T_P_B.objects.create(button=b, page_test=pt_obj,
                                    #                                          is_working=t_p_b.get('is_working',None))
                                    #
                                    #                     # global_working_percentage
                                    #                     total_tpb1 = T_P_B.objects.filter(button=b).count()
                                    #                     global_working_percentage_tpb = None
                                    #                     if total_tpb1 > 0:
                                    #                         working_tpb1 = T_P_B.objects.filter(button=b,
                                    #                                                             is_working=True).count()
                                    #                         global_working_percentage_tpb = working_tpb1 / total_tpb1 * 100.0
                                    #
                                    #                     # local working percentage
                                    #                     d2 = datetime.today() - timedelta(days=30)
                                    #                     tl = Test.objects.filter(date__gte=d2)
                                    #                     pt = Page_Test.objects.filter(page=p_obj, test__in=tl)
                                    #                     total_tpb2 = T_P_B.objects.filter(button=b,
                                    #                                                       page_test__in=pt).count()
                                    #                     last_month_working_percentage_tpb = None
                                    #                     if total_tpb2 > 0:
                                    #                         working_tpb2 = T_P_B.objects.filter(button=b,
                                    #                                                             page_test__in=pt,
                                    #                                                             is_working=True).count()
                                    #                         last_month_working_percentage_tpb = working_tpb2 / total_tpb2 * 100.0
                                    #
                                    #                         b.last_month_working_percentage = last_month_working_percentage_tpb
                                    #                         b.global_working_percentage = global_working_percentage_tpb
                                    #                         b.save()

                    if batches_list is not None:
                        for b_data in batches_list:
                            if b_data is not None:
                                p_a = b_data.get('page_address',None)
                                if p_a is not None:
                                    addr = p_a.get('address',None)
                                    if addr is not None:
                                        page = Page.objects.filter(address=addr)
                                        if len(page) > 0:
                                            Batch.objects.create(test=t_obj, levels=b_data.get('levels',None), page=page[0])
                                        else:
                                            p1 = Page.objects.create(address=addr)
                                            p1.save()
                                            Batch.objects.create(test=t_obj, levels=b_data.get('levels', None), page=p1)

        return user


class Page_For_ClientSerializer(serializers.ModelSerializer):
    min_download_time = serializers.SerializerMethodField('min_download_time_calc')
    max_download_time = serializers.SerializerMethodField('max_download_time_calc')

    def min_download_time_calc(self, obj):
        min_time=Page_Test.objects.filter(page=obj.pk).aggregate(Min('download_time'))
        return min_time.get('download_time__min',None)

    def max_download_time_calc(self, obj):
        max_time=Page_Test.objects.filter(page=obj.pk).aggregate(Max('download_time'))
        return max_time.get('download_time__max',None)

    class Meta:
        model=Page
        fields=('address','avg_download_time','min_download_time','max_download_time','global_working_percentage',
                'last_month_working_percentage',)















