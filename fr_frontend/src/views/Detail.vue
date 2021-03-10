<template>
  <div>
    <el-container>
      <el-main class="main" id="main" v-loading="loading">
        <div class="title">
          <el-col :span="14">
            <el-card class="box-card">
              <template #header>
                <div class="card-header">
                  <span
                    >事件-{{ sn }}：【{{ eventData.level_display }}】{{
                      eventData.name
                    }}！</span
                  >
                  <el-dropdown @command="handleCommand" class="nonprint">
                    <span class="el-dropdown-link nonprint">
                      操作<span v-if="refreshTimer">(自动刷新中)</span
                      ><i class="el-icon-arrow-down el-icon--right"></i>
                    </span>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item icon="el-icon-share" command="share"
                          >分享</el-dropdown-item
                        >
                        <el-dropdown-item
                          icon="el-icon-edit"
                          v-if="edit"
                          command="edit"
                          >编辑</el-dropdown-item
                        >
                        <el-dropdown-item
                          icon="el-icon-circle-close"
                          command="close"
                          v-if="edit"
                          >关闭</el-dropdown-item
                        >
                        <el-dropdown-item
                          icon="el-icon-printer"
                          command="pdf"
                          v-if="!edit"
                          >导出报告</el-dropdown-item
                        >
                        <el-dropdown-item
                          icon="el-icon-refresh"
                          command="refresh"
                          v-if="edit"
                          >自动刷新(一分钟)</el-dropdown-item
                        >
                        <el-dropdown-item icon="el-icon-s-home" command="home"
                          >返回首页</el-dropdown-item
                        >
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
              </template>
              <div class="text item">
                故障等级：
                <el-tag :type="stateColor[eventData.level_display]">{{
                  eventData.level_display
                }}</el-tag>
              </div>
              <div class="text item">
                故障发生时间： {{ eventData.occurrence_date }}
              </div>
              <div class="text item">
                涉及系统： {{ eventData.related_resources }}
              </div>
              <div class="text item">
                当前状态：
                <el-tag>{{ eventData.current_state_display }}</el-tag>
              </div>
              <div class="text item">
                当前处理人： {{ eventData.current_operator }}
              </div>
              <el-divider content-position="left" v-if="eventData.description"
                >其他信息</el-divider
              >
              <div class="text item">
                {{ eventData.description }}
              </div>
              <el-divider content-position="left">MTTR 信息一览</el-divider>
              <div class="text item">
                故障发现时间（MTTI）： {{ mttr.mtti }}
              </div>
              <div class="text item">
                故障定位时间（MTTK）： {{ mttr.mttk }}
              </div>
              <div class="text item">
                故障恢复时间（MTTF）： {{ mttr.mttf }}
              </div>
              <div class="text item">
                故障验证时间（MTTV）： {{ mttr.mttv }}
              </div>
            </el-card>
          </el-col>
        </div>
        <div class="timeline">
          <el-col :span="12">
            <el-button
              type="text"
              class="button nonprint"
              v-if="edit"
              @click="dialogRecordFormVisible = true"
              >新增记录</el-button
            >
            <el-timeline>
              <el-timeline-item
                :timestamp="item.created"
                v-bind:key="item.id"
                v-for="(item, index) in eventData.records"
                placement="top"
              >
                <el-card>
                  <h4>
                    <el-tag type="default">{{ item.state_display }}</el-tag>
                    {{ item.title }}
                  </h4>
                  <p>{{ item.description }}</p>
                  <div class="bottom">
                    <span class="time" v-if="item.current_operator"
                      >操作人: {{ item.current_operator }}</span
                    >
                    <span class="time">记录人：{{ item.created_by }}</span>
                    <el-button
                      type="text"
                      class="button nonprint"
                      v-if="edit"
                      @click="editRecord(item, index)"
                      >编辑</el-button
                    >
                  </div>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </el-col>
        </div>
        <el-backtop></el-backtop>
        <el-dialog title="事件信息" v-model="dialogInfoFormVisible">
          <el-form
            :model="infoForm"
            :rules="infoRules"
            ref="infoForm"
            label-width="120px"
          >
            <el-form-item label="名称" prop="name">
              <el-input
                v-model="infoForm.name"
                placeholder="请简要描述事件"
              ></el-input>
            </el-form-item>
            <el-form-item label="等级" prop="level">
              <el-select v-model="infoForm.level" placeholder="请选择等级">
                <el-option
                  :label="item.label"
                  :value="item.value"
                  :key="item.value"
                  v-for="item in levelOptions"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="发生时间" prop="occurrence_date">
              <el-date-picker
                v-model="infoForm.occurrence_date"
                type="datetime"
                placeholder="选择日期时间"
              >
              </el-date-picker>
            </el-form-item>
            <el-form-item label="当前处理人" prop="current_operator">
              <el-input
                v-model="infoForm.current_operator"
                placeholder="多项以逗号分隔"
              ></el-input>
            </el-form-item>
            <el-form-item label="涉及服务" prop="related_resources">
              <el-input
                v-model="infoForm.related_resources"
                placeholder="多项以逗号分隔"
              ></el-input>
            </el-form-item>
            <el-form-item label="其他信息" prop="description">
              <el-input
                v-model="infoForm.description"
                type="textarea"
                :rows="3"
              ></el-input>
            </el-form-item>
          </el-form>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="cancelInfoForm">取 消</el-button>
              <el-button type="primary" @click="submitInfoForm"
                >确 定</el-button
              >
            </span>
          </template>
        </el-dialog>
        <el-dialog title="记录信息" v-model="dialogRecordFormVisible">
          <el-form
            :rules="recordRules"
            :model="recordForm"
            ref="recordForm"
            label-width="120px"
          >
            <el-form-item label="名称" prop="title">
              <el-input
                v-model="recordForm.title"
                placeholder="请简要描述"
              ></el-input>
            </el-form-item>
            <el-form-item label="状态" prop="state">
              <el-select v-model="recordForm.state" placeholder="请选择状态">
                <el-option
                  :label="item.label"
                  :value="item.value"
                  :key="item.value"
                  v-for="item in tagOptions"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="操作人" prop="current_operator">
              <el-input
                v-model="recordForm.current_operator"
                placeholder="请输入操作人"
              ></el-input>
            </el-form-item>
            <el-form-item label="描述信息" prop="description">
              <el-input
                v-model="recordForm.description"
                type="textarea"
                :rows="3"
                placeholder="请输入详细内容"
              ></el-input>
            </el-form-item>
          </el-form>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="cancelRecordForm">取 消</el-button>
              <el-button type="primary" @click="submitRecordForm"
                >确 定</el-button
              >
            </span>
          </template>
        </el-dialog>
      </el-main>
    </el-container>
  </div>
</template>
<script>
import { copyText } from 'vue3-clipboard'
import jsPDF from 'jspdf'
import 'jspdf-autotable'

// @ is an alias to /src
import {
  getEventDetail,
  editEventDetail,
  addRecord,
  editRecordDetail,
} from '@api/events'

export default {
  name: 'Detail',
  data() {
    return {
      sn: '',
      loading: true,
      edit: false,
      username: '',
      eventData: {},
      mttr: {},
      dialogInfoFormVisible: false,
      infoForm: {
        name: '',
        level: '0',
        occurrence_date: '',
        current_operator: '',
        related_resources: '',
        description: '',
      },
      infoRules: {
        name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
        level: [{ required: true, message: '请选择等级', trigger: 'change' }],
        occurrence_date: [
          {
            type: 'date',
            required: true,
            message: '请选择发生日期',
            trigger: 'change',
          },
        ],
      },
      dialogRecordFormVisible: false,
      recordForm: {
        title: '',
        state: '',
        current_operator: '',
        description: '',
      },
      recordRules: {
        title: [{ required: true, message: '请简要说明事件', trigger: 'blur' }],
        state: [{ required: true, message: '请选择状态', trigger: 'change' }],
        current_operator: [
          { required: true, message: '请填写操作人', trigger: 'blur' },
        ],
      },
      tagOptions: [
        {
          value: 0,
          label: '打开',
        },
        {
          value: 1,
          label: '定位中',
        },
        {
          value: 2,
          label: '线上已恢复',
        },
        {
          value: 3,
          label: '解决中',
        },
        {
          value: 4,
          label: '上线中',
        },
        {
          value: 5,
          label: '观察中',
        },
        {
          value: 6,
          label: '结束',
        },
      ],
      levelOptions: [
        {
          value: 0,
          label: '紧急',
        },
        {
          value: 1,
          label: '中等',
        },
        {
          value: 2,
          label: '一般',
        },
      ],
      stateColor: {
        紧急: 'danger',
        一般: 'info',
        中等: 'warning',
      },
      refreshTimer: null, //定时器名称
    }
  },
  components: {},
  methods: {
    init() {
      this.sn = this.$route.params.id
      if (!this.sn || this.sn.length < 1) {
        this.$message.error('参数错误')
      }
      console.log('sn: ', this.sn)
      this._getData()
    },
    handleCommand(command) {
      if (command == 'edit') {
        this.dialogInfoFormVisible = true
        this.infoForm = {
          id: this.eventData.sn,
          name: this.eventData.name,
          level: this.eventData.level,
          occurrence_date: this.eventData.occurrence_date,
          current_operator: this.eventData.current_operator,
          related_resources: this.eventData.related_resources,
          description: this.eventData.description,
        }
      } else if (command == 'home') {
        this.$router.push({ name: 'Home' })
      } else if (command == 'close') {
        this.$confirm('此操作将会关闭事件, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        })
          .then(() => {
            this.closeEvent()
          })
          .catch(() => {
            this.$message({
              type: 'info',
              message: '已取消',
            })
          })
      } else if (command == 'pdf') {
        console.log('pdf')
        this.$message.info('开始生成，请稍等')
        this.loading = true
        let that = this
        setTimeout(function() {
          that.exportPDF()
        }, 1000)
      } else if (command == 'share') {
        copyText(window.location.href, undefined, (error, event) => {
          if (error) {
            this.$message.success('拷贝失败，请从浏览器中拷贝网址！')
            console.log(error)
          } else {
            this.$message.success('链接已拷贝！')
            console.log(event)
          }
        })
      } else if (command == 'refresh') {
        this.refreshData()
      }
    },
    editRecord(item, index) {
      this.recordForm = Object.assign({}, item)
      this.recordForm['index'] = index
      this.dialogRecordFormVisible = true
    },
    _getData() {
      this.loading = true
      getEventDetail(this.sn)
        .then((res) => {
          console.log(res)
          this.eventData = res
          this.mttr = res.mttr
          this.loading = false
          document.title = this.eventData.sn + '_' + this.eventData.name
        })
        .catch((e) => {
          console.log(e)
        })
    },
    cancelRecordForm() {
      this.$refs['recordForm'].resetFields()
      this.dialogRecordFormVisible = false
      this.recordForm = {
        title: '',
        tag: '',
        current_operator: '',
        description: '',
      }
    },
    submitRecordForm() {
      this.$refs['recordForm'].validate((valid) => {
        if (valid) {
          let data = {
            event: this.eventData.id,
            ...this.recordForm,
          }
          if (this.recordForm.id) {
            editRecordDetail(data)
              .then((res) => {
                console.log(res)
                this.$message.success('修改成功')
                this.eventData.records[this.recordForm.index] = res
                this.eventData.current_state = res.state
                this.eventData.current_state_display = res.state_display
                this.cancelRecordForm()
              })
              .catch((e) => {
                // eslint-disable-next-line no-prototype-builtins
                if (e.hasOwnProperty('data')) {
                  this.$message.error(JSON.stringify(e.data))
                } else {
                  this.$message.error(JSON.stringify(e))
                }
                // console.log(e)
              })
          } else {
            addRecord(data)
              .then((res) => {
                if (res) {
                  this.$message.success('添加成功')
                  this.eventData.records.splice(0, 0, res)
                  this.eventData.current_state = res.state
                  this.eventData.current_state_display = res.state_display
                  this.cancelRecordForm()
                } else {
                  // Cookies.set('access', 0);
                  console.log('res:', res)
                }
              })
              .catch((e) => {
                if (Object.prototype.hasOwnProperty.call(e, 'data')) {
                  this.$message.error(JSON.stringify(e.data))
                } else {
                  console.log(e)
                  this.$message.error('添加错误')
                }
              })
          }
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    cancelInfoForm() {
      this.$refs['infoForm'].resetFields()
      this.dialogInfoFormVisible = false
    },
    submitInfoForm() {
      this.$refs['infoForm'].validate((valid) => {
        if (valid) {
          editEventDetail(this.infoForm)
            .then((res) => {
              if (res) {
                this.eventData = res
                this.$message({
                  type: 'success',
                  message: '修改成功!',
                })
                this.cancelInfoForm()
              } else {
                // Cookies.set('access', 0);
                console.log('res:', res)
              }
            })
            .catch((e) => {
              if (Object.prototype.hasOwnProperty.call(e, 'data')) {
                this.$message.error(JSON.stringify(e.data))
              } else {
                console.log(e)
                this.$message.error('添加错误')
              }
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    closeEvent() {
      let data = {
        id: this.eventData.sn,
        current_state: 6,
      }
      editEventDetail(data)
        .then((res) => {
          console.log(res)
          this.eventData = res
          this.$message.success('关闭成功')
        })
        .catch((e) => {
          if (Object.prototype.hasOwnProperty.call(e, 'data')) {
            this.$message.error(JSON.stringify(e.data))
          } else {
            console.log(e)
            this.$message.error('关闭错误')
          }
        })
    },
    exportPDF() {
      Date.prototype.format = function(fmt) {
        var o = {
          'M+': this.getMonth() + 1, //月份
          'd+': this.getDate(), //日
          'h+': this.getHours(), //小时
          'm+': this.getMinutes(), //分
          's+': this.getSeconds(), //秒
          'q+': Math.floor((this.getMonth() + 3) / 3), //季度
          S: this.getMilliseconds(), //毫秒
        }
        if (/(y+)/.test(fmt)) {
          fmt = fmt.replace(
            RegExp.$1,
            (this.getFullYear() + '').substr(4 - RegExp.$1.length)
          )
        }
        for (var k in o) {
          if (new RegExp('(' + k + ')').test(fmt)) {
            fmt = fmt.replace(
              RegExp.$1,
              RegExp.$1.length == 1
                ? o[k]
                : ('00' + o[k]).substr(('' + o[k]).length)
            )
          }
        }
        return fmt
      }

      var doc = new jsPDF('p', 'pt', 'a4')

      doc.addFont(
        'static/fonts/SourceHanSans-Normal.ttf',
        'SourceHanSans',
        'nomarl'
      )

      doc.setFont('SourceHanSans', 'nomarl') // set font

      doc.setFontSize(42)
      doc.text(300, 300, '生产事故报告', 'center')

      doc.setFontSize(14)
      doc.setTextColor(150)
      doc.text(300, 340, '事件编号：' + this.eventData.sn, 'center')
      doc.setFontSize(14)
      doc.setTextColor(150)
      doc.text(
        300,
        360,
        '生成时间：' + new Date().format('yyyy-MM-dd hh:mm:ss'),
        'center'
      )
      doc.setFontSize(14)
      doc.setTextColor(150)
      doc.text(
        300,
        380,
        '操作人：' + this.$store.getters.getUsername || '访客',
        'center'
      )
      doc.setTextColor('black')
      doc.addPage()

      doc.setFontSize(22)
      doc.text(30, 60, '事件：' + this.eventData.sn)

      doc.setFontSize(16)
      doc.text(30, 100, '一，事件信息')

      doc.autoTable({
        // autoTable调用 ，font:中修改为自定义字体名称，注意：fontStyle需要与addFont中的类型对应。
        styles: {
          fillColor: 255,
          font: 'SourceHanSans',
          fontStyle: 'normal',
          textColor: 80,
          halign: 'left',
        }, // 表格样式
        columnStyles: { overflow: 'linebreak' },
        theme: 'striped', // 主题
        headStyles: {
          textColor: 255,
          fillColor: [41, 128, 185],
          fontStyle: 'bold',
        }, // 表头样式
        footStyles: {
          textColor: 255,
          fillColor: [41, 128, 185],
          fontStyle: 'bold',
        },
        alternateRowStyles: { fillColor: 245 },
        startY: 120, // 距离上边距离
        pageBreak: 'auto',
        rowPageBreak: 'avoid',
        body: [
          // 表格体
          { item: '故障等级', value: this.eventData.level_display },
          { item: '故障发生时间', value: this.eventData.occurrence_date },
          { item: '涉及系统', value: this.eventData.related_resources },
          { item: '当前状态', value: this.eventData.current_state_display },
          { item: '当前处理人', value: this.eventData.current_operator },
          { item: '故障发现时间（MTTI）', value: this.mttr.mtti },
          { item: '故障定位时间（MTTK）', value: this.mttr.mttk },
          { item: '故障恢复时间（MTTF）', value: this.mttr.mttf },
          { item: '故障验证时间（MTTV）', value: this.mttr.mttv },
          { item: '其他信息', value: this.eventData.description },
        ], // tableDate
        columns: [
          // 表头
          { header: '事项', dataKey: 'item' },
          { header: '说明', dataKey: 'value' },
        ],
      })

      doc.text(30, 500, '二，事件记录')

      doc.autoTable({
        // autoTable调用 ，font:中修改为自定义字体名称，注意：fontStyle需要与addFont中的类型对应。
        styles: {
          fillColor: 255,
          font: 'SourceHanSans',
          fontStyle: 'normal',
          textColor: 80,
          halign: 'left',
        }, // 表格样式
        columnStyles: { overflow: 'linebreak' },
        theme: 'striped', // 主题
        headStyles: {
          textColor: 255,
          fillColor: [41, 128, 185],
          fontStyle: 'bold',
        }, // 表头样式
        footStyles: {
          textColor: 255,
          fillColor: [41, 128, 185],
          fontStyle: 'bold',
        },
        alternateRowStyles: { fillColor: 245 },
        startY: 520, // 距离上边距离
        margin: { top: 10 },
        body: this.eventData.records, // tableDate
        pageBreak: 'auto',
        rowPageBreak: 'avoid',
        columns: [
          // 表头
          { header: '时间', dataKey: 'created' },
          { header: '状态', dataKey: 'state_display' },
          { header: '标题', dataKey: 'title' },
          { header: '记录人', dataKey: 'created_by' },
          { header: '操作人', dataKey: 'current_operator' },
          { header: '描述', dataKey: 'description' },
        ],
      })
      doc.save(this.eventData.sn + '.pdf', { returnPromise: true }).then(() => {
        this.loading = false
        this.$message.success('生成成功！')
      })
    },
    refreshData() {
      if (this.refreshTimer) {
        this.clearRefreshTimer()
      } else {
        this.refreshTimer = setInterval(() => {
          this._getData()
        }, 60000)
        this.$message.info('开启自动刷新！')
      }
    },
    clearRefreshTimer() {
      if (this.refreshTimer) {
        clearInterval(this.refreshTimer)
        this.refreshTimer = null
        this.$message.info('取消自动刷新！')
      }
    },
  },
  created() {
    this.init()
  },
  computed: {
    loginState: function() {
      // 通过vuex的getters方法来获取state里面的数据
      let username = this.$store.getters.getUsername
      return username && username.length > 0
    },
    current_state: function() {
      return this.eventData.current_state
    },
  },
  watch: {
    current_state: function(val) {
      console.log('事件状态:', val)
      this.edit = this.loginState && val != 6
      if (val == 6) {
        this.clearRefreshTimer()
      }
    },
  },
  beforeUnmount() {
    this.clearRefreshTimer()
  },
}
</script>
<style scoped>
.main {
  width: 100%;
}
.title {
  justify-content: center;
  align-items: center;
  display: -webkit-flex;
}
.timeline {
  justify-content: center;
  align-items: center;
  display: -webkit-flex;
  margin-top: 50px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}
.time {
  font-size: 13px;
  color: #999;
}
.bottom {
  margin-top: 13px;
  line-height: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.el-dropdown-link {
  cursor: pointer;
  color: #409eff;
}
.el-icon-arrow-down {
  font-size: 12px;
}
@media print {
  .page-break {
    page-break-after: always;
  }
  .nonprint {
    display: none;
  }
}
</style>
