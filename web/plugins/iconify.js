import Vue from "vue";

import IconifyIcon from '@iconify/vue';

// Страница login
import bxUser from '@iconify/icons-bx/bx-user';
import lockPasswordLine from '@iconify/icons-ri/lock-password-line';
// Страница login

// Боковая панель
import monitorIcon from "@iconify/icons-feather/monitor";
import reportIcon from '@iconify/icons-carbon/report';
import dataStructured from '@iconify/icons-carbon/data-structured';

import dashboard3Line from '@iconify/icons-ri/dashboard-3-line';
import calendar4Event from '@iconify/icons-bi/calendar4-event';
import guyUser from '@iconify/icons-ps/guy-user';
// Боковая панель

// Header иконки
import roundSettings from "@iconify/icons-ic/round-settings";
import errorWarningFill from '@iconify/icons-ri/error-warning-fill';
import baselineAccountCircle from '@iconify/icons-ic/baseline-account-circle';
// Header иконки

// стрелка вверх-вниз общая
import baselineKeyboardArrowDown from '@iconify/icons-ic/baseline-keyboard-arrow-down';
// стрелка вверх-вниз общая

//sub-панель
import outlineArrowBackIos from '@iconify/icons-ic/outline-arrow-back-ios';
import outlineArrowForwardIos from '@iconify/icons-ic/outline-arrow-forward-ios';

import baselineViewHeadline from '@iconify/icons-ic/baseline-view-headline';
import baselineViewStream from '@iconify/icons-ic/baseline-view-stream';
import baselineExtension from '@iconify/icons-ic/baseline-extension';
//sub-панель

//страница редактирования проекта
import addIcon from '@iconify/icons-carbon/add';
import editOutlined from '@iconify/icons-ant-design/edit-outlined';
import baselineRemove from '@iconify/icons-ic/baseline-remove';
import bxSearchAlt2 from '@iconify/icons-bx/bx-search-alt-2';
//страница редактирования проекта


// окно данных пользователя
import outlineOpenInBrowser from '@iconify/icons-ic/outline-open-in-browser';
import baselineEdit from '@iconify/icons-ic/baseline-edit';
// окно данных пользователя

// иконка драйвера
import baselineFiberDvr from '@iconify/icons-ic/baseline-fiber-dvr';
// иконка драйвера

// toggle
import baselineToggleOff from '@iconify/icons-ic/baseline-toggle-off';
// toggle

//warning
import warningStandardLine from '@iconify/icons-clarity/warning-standard-line';

IconifyIcon.addIcon('bxUser', bxUser);
IconifyIcon.addIcon('lockPasswordLine', lockPasswordLine);

IconifyIcon.addIcon('monitorIcon', monitorIcon);
IconifyIcon.addIcon('reportIcon', reportIcon);
IconifyIcon.addIcon('dataStructured', dataStructured);

IconifyIcon.addIcon('dashboard3Line', dashboard3Line);
IconifyIcon.addIcon('calendar4Event', calendar4Event);
IconifyIcon.addIcon('guyUser', guyUser);

IconifyIcon.addIcon('roundSettings', roundSettings);
IconifyIcon.addIcon('errorWarningFill', errorWarningFill);
IconifyIcon.addIcon('baselineAccountCircle', baselineAccountCircle);
IconifyIcon.addIcon('baselineKeyboardArrowDown', baselineKeyboardArrowDown);

IconifyIcon.addIcon('outlineArrowBackIos', outlineArrowBackIos);
IconifyIcon.addIcon('outlineArrowForwardIos', outlineArrowForwardIos);

IconifyIcon.addIcon('baselineViewHeadline', baselineViewHeadline);
IconifyIcon.addIcon('baselineViewStream', baselineViewStream);
IconifyIcon.addIcon('baselineExtension', baselineExtension);


IconifyIcon.addIcon('addIcon', addIcon);
IconifyIcon.addIcon('editOutlined', editOutlined);
IconifyIcon.addIcon('baselineRemove', baselineRemove);
IconifyIcon.addIcon('bxSearchAlt2', bxSearchAlt2);

IconifyIcon.addIcon('outlineOpenInBrowser', outlineOpenInBrowser);
IconifyIcon.addIcon('baselineEdit', baselineEdit);

IconifyIcon.addIcon('baselineFiberDvr', baselineFiberDvr);

IconifyIcon.addIcon('baselineToggleOff', baselineToggleOff);

IconifyIcon.addIcon('warningStandardLine', warningStandardLine);


Vue.use(IconifyIcon);
