import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Box,
  Typography,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  School as CoursesIcon,
  AttachMoney as FinancialIcon,
  People as TeamIcon,
  Campaign as CampaignsIcon,
  Person as StudentsIcon,
  Handshake as PartnersIcon,
  Telegram as TelegramIcon,
  Create as ContentIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const drawerWidth = 240;

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
  { text: 'Курсы', icon: <CoursesIcon />, path: '/courses' },
  { text: 'Финансы', icon: <FinancialIcon />, path: '/financial' },
  { text: 'Команда', icon: <TeamIcon />, path: '/team' },
  { text: 'Кампании', icon: <CampaignsIcon />, path: '/campaigns' },
  { text: 'Студенты', icon: <StudentsIcon />, path: '/students' },
  { text: 'Партнеры', icon: <PartnersIcon />, path: '/partners' },
  { text: 'Telegram Bot', icon: <TelegramIcon />, path: '/telegram' },
  { text: 'Генератор контента', icon: <ContentIcon />, path: '/content' },
];

const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
        },
      }}
    >
      <Box sx={{ overflow: 'auto', mt: 8 }}>
        <Box sx={{ p: 2 }}>
          <Typography variant="h6" color="primary">
            Online Classes
          </Typography>
        </Box>
        <Divider />
        <List>
          {menuItems.map((item) => (
            <ListItem key={item.text} disablePadding>
              <ListItemButton
                selected={location.pathname === item.path}
                onClick={() => navigate(item.path)}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Box>
    </Drawer>
  );
};

export default Sidebar; 