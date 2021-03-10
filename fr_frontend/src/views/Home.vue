<template>
  <div>
    <el-container>
      <el-main class="main">
        <el-row type="flex" class="row-bg" justify="end">
          <el-col :span="4">
            <el-dropdown @command="menuClick">
              <span class="el-dropdown-link">
                {{ username }}<i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="login" v-if="!loginState"
                    >登录</el-dropdown-item
                  >
                  <el-dropdown-item command="admin" v-if="loginState"
                    >后台</el-dropdown-item
                  >
                  <el-dropdown-item command="logout" v-if="loginState"
                    >登出</el-dropdown-item
                  >
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </el-col>
        </el-row>
        <div class="title">
          <h2>事故列表</h2>
        </div>
        <div class="info">
          <el-col :span="16">
            <div style="margin-bottom: 20px">
              <el-button @click="dialogInfoFormVisible = true" v-if="loginState"
                >新增</el-button
              >
            </div>
            <el-table
              :data="tableData"
              border
              style="width: 100%"
              v-loading="loading"
              :key="reflush"

            >
              <el-table-column
                prop="created"
                label="创建日期"
                sortable
                width="180"
              >
              </el-table-column>
              <el-table-column
                prop="occurrence_date"
                label="发生日期"
                sortable
                width="180"
              >
              </el-table-column>
              <el-table-column prop="sn" label="事件编号" sortable width="180">
                <template #default="scope">
                  <router-link
                    :to="{ name: 'Detail', params: { id: scope.row.sn } }"
                    style="text-decoration:none"
                  >
                    <el-link type="primary">{{ scope.row.sn }}</el-link>
                  </router-link>
                </template>
              </el-table-column>
              <el-table-column prop="name" label="名称"> </el-table-column>
              <el-table-column prop="level" label="等级" sortable width="80">
                <template #default="scope">
                  <el-tag size="medium" :type="stateColor[scope.row.level_display]">{{
                    scope.row.level_display
                  }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column
                prop="current_state_display"
                label="当前状态"
                sortable
                width="120"
              >
                <template #default="scope">
                  <el-tag size="medium">{{ scope.row.current_state_display }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column
                prop="current_operator"
                label="当前处理人"
                sortable
                width="180"
              >
              </el-table-column>
            </el-table>
            <div style="margin-top: 20px; float:right">
              <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page="currentPage"
                :page-sizes="pageSizes"
                :page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper"
                :total="dataTotal"
                v-if="tableData.length > 0"
              >
              </el-pagination>
            </div>
          </el-col>
        </div>
        <el-backtop></el-backtop>
      </el-main>
      <el-dialog title="登录" v-model="dialogLoginFormVisible" width="20%">
        <el-form
          :model="loginForm"
          :rules="loginRules"
          ref="loginForm"
          label-width="80px"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="loginForm.username"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="loginForm.password" show-password></el-input>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="cancelLoginForm">取 消</el-button>
            <el-button type="primary" @click="submitLoginForm">确 定</el-button>
          </span>
        </template>
      </el-dialog>
      <el-dialog title="新增事件" v-model="dialogInfoFormVisible">
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
            <el-button type="primary" @click="submitInfoForm">确 定</el-button>
          </span>
        </template>
      </el-dialog>
    </el-container>
  </div>
</template>

<script>
// @ is an alias to /src
// import Cookies from 'js-cookie';
import { getEventList, addEvent } from '@api/events'
import { login, logout } from '@api/users'
import { mapActions } from 'vuex'

export default {
  name: 'Home',
  data() {
    return {
      loading: true,
      tableData: [],
      reflush: 1,
      dialogLoginFormVisible: false,
      loginForm: {
        username: '',
        password: '',
      },
      loginRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
        ],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
      },
      dialogInfoFormVisible: false,
      infoForm: {
        name: '',
        level: 0,
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
        current_operator: [
          { required: true, message: '请输入当前操作人', trigger: 'blur' },
        ],
        related_resources: [
          { required: true, message: '请输入关联资源', trigger: 'blur' },
        ],
      },
      currentPage: 1,
      pageSize: 10,
      pageSizes: [10, 30, 50, 100, 200],
      dataTotal: 10,
      search: '',
      username: '访客',
      levelOptions:[{
          value: 0,
          label: '紧急'
        }, {
          value: 1,
          label: '中等'
        }, {
          value: 2,
          label: '一般'
        }],
      stateColor: {
        '紧急': 'danger',
        '一般': 'info',
        '中等': 'warning',
      }
    }
  },
  components: {},
  methods: {
    init() {
      this._getEventData()
    },
    _getEventData() {
      this.loading = true
      getEventList(this.search, this.currentPage, this.pageSize)
        .then((res) => {
          this.tableData = res.results
          this.dataTotal = res.count
          this.reflush = Math.random()
          this.loading = false
        })
        .catch((e) => {
          console.log(e)
        })
    },
    handleSizeChange(val) {
      this.pageSize = val
      this._getEventData()
      console.log(`每页 ${val} 条`)
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this._getEventData()
      console.log(`当前页: ${val}`)
    },
    cancelLoginForm() {
      this.$refs['loginForm'].resetFields()
      this.dialogLoginFormVisible = false
    },
    submitLoginForm() {
      this.$refs['loginForm'].validate((valid) => {
        if (valid) {
          login(this.loginForm)
            .then((res) => {
              if (res.data.token) {
                // 调用vuex的ations设置城市的值
                // this.$store.dispatch("saveUserInfo", res.data);
                this.saveUserInfo(res.data)
                this.loginState = true
                this.$message.success('登录成功')
                this.cancelLoginForm()
              } else {
                // Cookies.set('access', 0);
                console.log('res:', res)
              }
            })
            .catch((e) => {
              // eslint-disable-next-line no-prototype-builtins
              if (e.data.hasOwnProperty('non_field_errors')) {
                this.$message.error(e.data.non_field_errors[0])
                // this.$refs.loginForm.resetFields();
              } else {
                this.$message.error('用户名或密码错误')
              }
              // console.log(e)
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    setUsername(name) {
      this.username = name ? name : '访客'
    },
    menuClick(command) {
      if (command == 'login') {
        console.log('login')
        this.dialogLoginFormVisible = true
      } else if (command == 'logout') {
        this.$confirm('此操作将退出登录, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        })
          .then(() => {
            logout()
              .then((res) => {
                console.log(res)
                this.removeUserInfo()
                this.$message({
                  type: 'success',
                  message: '登出成功!',
                })
              })
              .catch((e) => {
                if (
                  Object.prototype.hasOwnProperty.call(
                    e.data,
                    'non_field_errors'
                  )
                ) {
                  this.$message.error(e.data.non_field_errors[0])
                } else {
                  this.$message.error('登出错误')
                }
              })
          })
          .catch(() => {
            this.$message({
              type: 'info',
              message: '已取消登出',
            })
          })
      } else if (command == 'admin') {
        window.open(process.env.BASE_URL + "/admin")
      }
    },
    cancelInfoForm() {
      this.$refs['infoForm'].resetFields()
      this.dialogInfoFormVisible = false
    },
    submitInfoForm() {
      this.$refs['infoForm'].validate((valid) => {
        if (valid) {
          addEvent(this.infoForm)
            .then((res) => {
              if (res) {
                this.tableData.splice(0, 0, res)
                this.reflush = Math.random()
                this.dataTotal += 1
                this.$message({
                  type: 'success',
                  message: '添加成功!',
                })
                this.cancelInfoForm()
              } else {
                // Cookies.set('access', 0);
                console.log('res:', res)
              }
            })
            .catch((e) => {
              console.log(e)
              if (Object.prototype.hasOwnProperty.call(e,'non_field_errors')) {
                this.$message.error(e.data.non_field_errors[0])
                // this.$refs.loginForm.resetFields();
              } else {
                this.$message.error('添加错误')
              }
              
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    ...mapActions(['saveUserInfo', 'removeUserInfo']),
  },
  created() {
    this.init()
  },
  computed: {
    loginState: function() {
      // 通过vuex的getters方法来获取state里面的数据
      let username = this.$store.getters.getUsername
      this.setUsername(username)
      return username && username.length > 0
    },
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
.info {
  justify-content: center;
  align-items: center;
  display: -webkit-flex;
  margin-top: 50px;
}
.menu {
  float: right;
}
.el-dropdown-link {
  cursor: pointer;
  color: #409eff;
}
.el-icon-arrow-down {
  font-size: 12px;
}
</style>
