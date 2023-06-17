
/*==============================================================*/
/* Table: SDGT_PROYECTO                                         */
/*==============================================================*/
create table SDGT_PROYECTO (
   PRO_ID               SERIAL               not null,
   PRO_NOMBRE           VARCHAR(100)         null,
   PRO_DESCRIPCION      TEXT                 null,
   PRO_ESTADO           VARCHAR(15)          null,
   constraint PK_SDGT_PROYECTO primary key (PRO_ID)
);

/*==============================================================*/
/* Table: SDGT_TAREA                                            */
/*==============================================================*/
create table SDGT_TAREA (
   TEA_ID               SERIAL               not null,
   PRO_ID               INT4                 null,
   USR_ID               INT4                 null,
   TEA_TITULO           VARCHAR(100)         null,
   TEA_DESCRIPCION      TEXT                 null,
   TEA_FECHAVENCIMIENTO DATE                 null,
   TEA_ESTADO           VARCHAR(15)          null,
   constraint PK_SDGT_TAREA primary key (TEA_ID)
);

/*==============================================================*/
/* Table: SDGT_USUARIO                                          */
/*==============================================================*/
create table SDGT_USUARIO (
   USR_ID               SERIAL               not null,
   USR_NOMBRE           VARCHAR(50)          null,
   USR_APELLIDO         VARCHAR(50)          null,
   USR_PASS             VARCHAR(256)         null,
   USR_EMAIL            VARCHAR(100)         null,
   USR_TIPO             INT4                 null,
   constraint PK_SDGT_USUARIO primary key (USR_ID)
);

alter table SDGT_TAREA
   add constraint FK_SDGT_TAR_REFERENCE_SDGT_PRO foreign key (PRO_ID)
      references SDGT_PROYECTO (PRO_ID)
      on delete restrict on update restrict;

alter table SDGT_TAREA
   add constraint FK_SDGT_TAR_REFERENCE_SDGT_USU foreign key (USR_ID)
      references SDGT_USUARIO (USR_ID)
      on delete restrict on update restrict;


INSERT INTO public.sdgt_usuario(
	usr_id, usr_nombre, usr_apellido, usr_pass, usr_email, usr_tipo)
	VALUES (0, 'Juan', 'Perez', '$2a$12$EK6ErKQOKSfjt6YMonXEQ.3z4Vni.wnSv6PpdrMbQ5n6T9jbyH/Ti', 'abc123@gmail.com', 1);

Email= abc123@gmail.com
Contraseña= holamundo
