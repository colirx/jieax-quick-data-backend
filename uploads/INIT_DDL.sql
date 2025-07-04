-- 租户表：仅存放租户信息
DROP TABLE IF EXISTS sys_tenant;
CREATE TABLE IF NOT EXISTS sys_tenant
(
    id            varchar(32) primary key comment '租户 ID',
    code          varchar(20) unique not null comment '租户编码',
    name          varchar(100)       not null comment '租户名称',
    parent_tenant varchar(32) comment '父级租户 ID',
    version       int                not null comment '版本号',
    created_user  varchar(32) comment '创建用户 ID',
    created_time  timestamp          not null comment '创建时间，保存为 UTC 时间',
    updated_user  varchar(32) comment '更新用户 ID',
    updated_time  timestamp          not null comment '更新时间，保存为 UTC 时间',
    is_deleted    boolean            not null comment '逻辑删除'
) ENGINE = INNODB comment '租户表：仅存放租户信息';

-- 机构类型表：仅存放组织类型信息
DROP TABLE IF EXISTS sys_organization_type;
CREATE TABLE IF NOT EXISTS sys_organization_type
(
    id           varchar(32) primary key comment '组织类型 ID',
    tenant_id    varchar(32)  not null comment '租户 ID',
    name         varchar(100) not null comment '组织类型名称',
    en_name      varchar(100) not null comment '组织类型英文名称',
    version      int          not null comment '版本号',
    created_user varchar(32) comment '创建用户 ID',
    created_time timestamp    not null comment '创建时间，保存为 UTC 时间',
    updated_user varchar(32) comment '更新用户 ID',
    updated_time timestamp    not null comment '更新时间，保存为 UTC 时间',
    is_deleted   boolean      not null comment '逻辑删除',
    foreign key (tenant_id) references sys_tenant (id)
) ENGINE = INNODB;

-- 机构表：仅存放机构信息，其中机构中存放租户 Id 作为关联项
DROP TABLE IF EXISTS sys_organization;
CREATE TABLE IF NOT EXISTS sys_organization
(
    id            varchar(32) primary key comment '组织 ID',
    tenant_id     varchar(32)        not null comment '租户 ID',
    code          varchar(20) unique not null comment '组织编码',
    name          varchar(100)       not null comment '组织名称',
    alias         varchar(100)       not null comment '组织别名',
    org_type_id   varchar(32)        not null comment '组织类型 ID',
    parent_org_id varchar(32) comment '父级组织 ID',
    version       int                not null comment '版本号',
    created_user  varchar(32) comment '创建用户 ID',
    created_time  timestamp          not null comment '创建时间，保存为 UTC 时间',
    updated_user  varchar(32) comment '更新用户 ID',
    updated_time  timestamp          not null comment '更新时间，保存为 UTC 时间',
    is_deleted    boolean            not null comment '逻辑删除',
    foreign key (tenant_id) references sys_tenant (id)
) ENGINE = INNODB comment '机构类型表：仅存放组织类型信息';

-- 雇员信息表：仅存放雇员个人基本信息
DROP TABLE IF EXISTS sys_user;
CREATE TABLE IF NOT EXISTS sys_user
(
    id               varchar(32) primary key comment '雇员 ID',
    id_card          varchar(17) comment '身份证号',
    code             varchar(20) unique not null comment '雇员编号',
    name             varchar(100)       not null comment '雇员姓名',
    sex              tinyint comment '性别, 0: 女, 1: 男',
    mobile           varchar(20) comment '手机号码',
    is_active        boolean comment '是否激活',
    password         varchar(100)       not null comment '登录密码',
    password_retries int                not null comment '用户重试密码次数, 三次失败后则根据策略规定锁定时间以及升级锁定时间',
    unlock_time      timestamp comment '用户解锁时间',
    version          int                not null comment '版本号',
    created_user     varchar(32) comment '创建用户 ID',
    created_time     timestamp          not null comment '创建时间，保存为 UTC 时间',
    updated_user     varchar(32) comment '更新用户 ID',
    updated_time     timestamp          not null comment '更新时间，保存为 UTC 时间',
    is_deleted       boolean            not null comment '逻辑删除'
) ENGINE = INNODB comment '雇员信息表：仅存放雇员个人基本信息';

-- 角色表：租户下设立角色表，用于本租户下的所有机构
DROP TABLE IF EXISTS sys_tenant_role;
CREATE TABLE IF NOT EXISTS sys_tenant_role
(
    id           varchar(32) primary key comment '角色 ID',
    tenant_id    varchar(32)  not null comment '所属租户 ID',
    name         varchar(100) not null comment '角色名称',
    en_name      varchar(100) comment '角色英文名称',
    type         varchar(20)  not null comment '角色类型',
    version      int          not null comment '版本号',
    created_user varchar(32) comment '创建用户 ID',
    created_time timestamp    not null comment '创建时间，保存为 UTC 时间',
    updated_user varchar(32) comment '更新用户 ID',
    updated_time timestamp    not null comment '更新时间，保存为 UTC 时间',
    is_deleted   boolean      not null comment '逻辑删除',
    foreign key (tenant_id) references sys_tenant (id)
) ENGINE = INNODB comment '角色表：租户下设立角色表，用于本租户下的所有机构';

-- 雇员-机构-角色表：雇员可以存放自己的所属机构信息，与机构表关联，得到机构与租户信息
DROP TABLE IF EXISTS sys_user_organization_relation;
CREATE TABLE IF NOT EXISTS sys_user_organization_relation
(
    user_id        varchar(32) not null comment '雇员 ID',
    tenant_role_id varchar(32) not null comment '租户角色 ID',
    org_id         varchar(32) not null comment '机构 ID',
    version        int         not null comment '版本号',
    created_user   varchar(32) comment '创建用户 ID',
    created_time   timestamp   not null comment '创建时间，保存为 UTC 时间',
    updated_user   varchar(32) comment '更新用户 ID',
    updated_time   timestamp   not null comment '更新时间，保存为 UTC 时间',
    is_deleted     boolean     not null comment '逻辑删除',
    foreign key (user_id) references sys_user (id),
    foreign key (tenant_role_id) references sys_tenant_role (id),
    foreign key (org_id) references sys_organization (id)
) ENGINE = INNODB comment '雇员-机构-角色表：雇员可以存放自己的所属机构信息，与机构表关联，得到机构与租户信息';

-- 项目组信息表：存放项目组信息，可以作为同部门以及跨部门协作的项目组使用
DROP TABLE IF EXISTS sys_organization_group;
CREATE TABLE IF NOT EXISTS sys_organization_group
(
    id           varchar(32) primary key comment '项目组 ID',
    org_id       varchar(32)        not null comment '机构 ID, 用于设定用户切换到哪个机构可以看到本项目',
    code         varchar(20) unique not null comment '项目组编号',
    name         varchar(32)        not null comment '项目组名称',
    version      int                not null comment '版本号',
    created_user varchar(32) comment '创建用户 ID',
    created_time timestamp          not null comment '创建时间，保存为 UTC 时间',
    updated_user varchar(32) comment '更新用户 ID',
    updated_time timestamp          not null comment '更新时间，保存为 UTC 时间',
    is_deleted   boolean            not null comment '逻辑删除',
    foreign key (org_id) references sys_organization (id)
) ENGINE = INNODB comment '项目组信息-雇员表：存放雇员信息，可以作为同部门以及跨部门协作的项目组使用';


-- 项目组信息-雇员表：存放雇员信息，可以作为同部门以及跨部门协作的项目组使用
DROP TABLE IF EXISTS sys_organization_group_user;
CREATE TABLE IF NOT EXISTS sys_organization_group_user
(
    id           varchar(32) primary key comment '唯一 key, 持有此 key 的人可以在任务中流转',
    group_id     varchar(32) not null comment '项目组 ID',
    user_id      varchar(32) not null comment '用户 ID',
    version      int         not null comment '版本号',
    created_user varchar(32) comment '创建用户 ID',
    created_time timestamp   not null comment '创建时间，保存为 UTC 时间',
    updated_user varchar(32) comment '更新用户 ID',
    updated_time timestamp   not null comment '更新时间，保存为 UTC 时间',
    is_deleted   boolean     not null comment '逻辑删除',
    unique (group_id, user_id),
    foreign key (user_id) references sys_user (id)
) ENGINE = INNODB comment '项目组信息-雇员表：存放雇员信息，可以作为同部门以及跨部门协作的项目组使用';

-- 任务表：存放任务信息表
DROP TABLE IF EXISTS sys_task;
CREATE TABLE IF NOT EXISTS sys_task
(
    id       varchar(32) primary key comment '任务 ID',
    group_id varchar(32)  not null comment '所属项目组 ID',
    name     varchar(100) not null comment '任务名称',
    code     varchar(20)  not null comment '任务编号',
    comment  text comment '任务描述, 以 JSON 形式存放数据',
    foreign key (group_id) references sys_organization_group (id)
) ENGINE = INNODB comment '任务表：存放任务信息表';

-- 任务-项目信息表：存放项目的流转信息，以及指定 key 的角色信息
DROP TABLE IF EXISTS sys_task_node;
CREATE TABLE IF NOT EXISTS sys_task_node
(
    id            varchar(32) primary key comment '任务节点 ID',
    group_user_id varchar(32) not null comment '所属项目组下唯一 key',
    node_group_id varchar(32) not null comment '节点组编号',
    next_node_id  varchar(32) comment '下个节点 ID',
    foreign key (group_user_id) references sys_organization_group_user (id)
) ENGINE = INNODB comment '任务-项目信息表：存放项目的流转信息，以及指定 key 的角色信息';

-- 任务角色表：用于分配给任务中人员权限
DROP TABLE IF EXISTS sys_task_role;
CREATE TABLE IF NOT EXISTS sys_task_role
(
    id           varchar(32) primary key comment '任务角色 ID',
    group_id     varchar(32)  not null comment '所属项目组 ID',
    name         varchar(100) not null comment '角色名称',
    en_name      varchar(100) comment '角色英文名称',
    type         varchar(20)  not null comment '角色类型',
    version      int          not null comment '版本号',
    created_user varchar(32) comment '创建用户 ID',
    created_time timestamp    not null comment '创建时间，保存为 UTC 时间',
    updated_user varchar(32) comment '更新用户 ID',
    updated_time timestamp    not null comment '更新时间，保存为 UTC 时间',
    is_deleted   boolean      not null comment '逻辑删除',
    foreign key (group_id) references sys_organization_group (id)
) ENGINE = INNODB comment '任务角色表：用于分配给任务中人员权限';

-- 项目组节点-任务角色表：用于分配给任务中人员权限
DROP TABLE IF EXISTS sys_group_node_role_relation;
CREATE TABLE IF NOT EXISTS sys_group_node_role_relation
(
    task_role_id varchar(32) not null comment '所属任务节点 ID',
    version      int         not null comment '版本号',
    created_user varchar(32) comment '创建用户 ID',
    created_time timestamp   not null comment '创建时间，保存为 UTC 时间',
    updated_user varchar(32) comment '更新用户 ID',
    updated_time timestamp   not null comment '更新时间，保存为 UTC 时间',
    is_deleted   boolean     not null comment '逻辑删除',
    foreign key (task_role_id) references sys_task_role (id)
) ENGINE = INNODB comment '项目组节点-任务角色表：用于分配给任务中人员权限';
