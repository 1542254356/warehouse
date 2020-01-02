CREATE TABLE app_goods
(
  goodsID        INTEGER     NOT NULL  PRIMARY KEY COMMENT '货物编号',
  goods_name     VARCHAR(20) NOT NULL COMMENT '货物名称',
  goods_price    REAL        NOT NULL COMMENT '货物成本',
  goods_sprice   REAL        NOT NULL COMMENT '货物售价',
  goods_discount REAL        NOT NULL COMMENT '折扣',
  goods_amount   INTEGER     NOT NULL COMMENT '在售数量',
  update_date    DATETIME    NOT NULL COMMENT '更新日期',
  goods_sup_id   INTEGER REFERENCES app_supplier (id) COMMENT '供应商名称'
)COMMENT '货物表/商品表';

CREATE INDEX app_goods_goods_sup_id
  ON app_goods (goods_sup_id);


CREATE TABLE app_stockout
(
  id            INTEGER  NOT NULL PRIMARY KEY AUTO_INCREMENT ,
  out_date      DATETIME NOT NULL COMMENT '出库时间',
  out_amount    INTEGER  NOT NULL COMMENT '出库数量',
  out_ps        VARCHAR(500) COMMENT '备注',
  goods_name_id INTEGER  NOT NULL  REFERENCES app_goods (goodsID) COMMENT '货物',
  res_person_id INTEGER  NOT NULL REFERENCES app_userinfo (id) COMMENT '经办人',
  sup_name_id   INTEGER  NOT NULL REFERENCES app_supplier (id) COMMENT '供应商'
) COMMENT '出库表';

CREATE INDEX app_stockout_goods_name_id
  ON app_stockout (goods_name_id);

CREATE INDEX app_stockout_res_person_id
  ON app_stockout (res_person_id);

CREATE INDEX app_stockout_sup_name_id
  ON app_stockout (sup_name_id);


CREATE TABLE app_storage
(
  goods_name_id  INTEGER NOT NULL PRIMARY KEY REFERENCES app_goods (goodsID) COMMENT '货物名称',
  storage_amount INTEGER COMMENT '现有库存',
  storage_max    INTEGER COMMENT '最大库存量',
  create_date    DATETIME COMMENT '更新日期'
) COMMENT '库存状况表';

CREATE TABLE app_supplier
(
  id       INTEGER     NOT NULL PRIMARY KEY AUTO_INCREMENT,
  supID    INTEGER COMMENT '供应商编号',
  sup_name VARCHAR(20) NOT NULL COMMENT '供应商名称',
  sup_tel  INTEGER COMMENT '供应商电话'
) COMMENT '供应商表';

CREATE TABLE app_userinfo
(
  id         INTEGER     NOT NULL PRIMARY KEY AUTO_INCREMENT,
  name       VARCHAR(10) COMMENT '姓名',
  sex        VARCHAR(10) NOT NULL COMMENT '性别',
  job        VARCHAR(10) NOT NULL COMMENT '职位',
  job_num    INTEGER     NOT NULL COMMENT '工号',
  account_id INTEGER UNIQUE REFERENCES auth_user (id) COMMENT '用户id'
)COMMENT '员工信息表';


CREATE TABLE app_wavehousing
(
  id            INTEGER  NOT NULL PRIMARY KEY AUTO_INCREMENT,
  in_date       DATETIME NOT NULL COMMENT '入库时间',
  in_price      REAL     NOT NULL COMMENT '入库单价',
  in_amount     INTEGER  NOT NULL COMMENT '入库数量',
  in_ps         VARCHAR(100) COMMENT '备注',
  goods_name_id INTEGER  NOT NULL REFERENCES app_goods (goodsID) COMMENT '货物',
  res_person_id INTEGER  NOT NULL REFERENCES app_userinfo (id) COMMENT '经办人',
  sup_name_id   INTEGER  NOT NULL REFERENCES app_supplier (id) COMMENT '供应商'
)COMMENT '入库表';

CREATE INDEX app_wavehousing_goods_name_id
  ON app_wavehousing (goods_name_id);

CREATE INDEX app_wavehousing_res_person_id
  ON app_wavehousing (res_person_id);

CREATE INDEX app_wavehousing_sup_name_id
  ON app_wavehousing (sup_name_id);


