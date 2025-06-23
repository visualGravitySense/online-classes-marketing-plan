import React, { useEffect, useState } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  TrendingUp,
  People,
  School,
  Campaign,
} from '@mui/icons-material';
import { DashboardSummary } from '@/types';
import { apiService } from '@/services/api';

const Dashboard: React.FC = () => {
  const [data, setData] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const summary = await apiService.getDashboardSummary();
        setData(summary);
      } catch (err) {
        setError('Ошибка загрузки данных');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  if (!data) {
    return <Alert severity="warning">Данные не найдены</Alert>;
  }

  const StatCard = ({ 
    title, 
    value, 
    icon, 
    color = 'primary.main',
    subtitle = ''
  }: {
    title: string;
    value: string | number;
    icon: React.ReactNode;
    color?: string;
    subtitle?: string;
  }) => (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box>
            <Typography color="textSecondary" gutterBottom variant="h6">
              {title}
            </Typography>
            <Typography variant="h4" component="div" color={color}>
              {value}
            </Typography>
            {subtitle && (
              <Typography variant="body2" color="textSecondary">
                {subtitle}
              </Typography>
            )}
          </Box>
          <Box color={color}>
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Панель управления
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Общий доход"
            value={`${data.financials.totalRevenue.toLocaleString()} ₽`}
            icon={<TrendingUp fontSize="large" />}
            color="success.main"
            subtitle={`Прибыль: ${data.financials.profitMargin}%`}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Курсы"
            value={data.courses.total}
            icon={<School fontSize="large" />}
            color="primary.main"
            subtitle={`Активных: ${data.courses.active}`}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Студенты"
            value={data.students.total}
            icon={<People fontSize="large" />}
            color="info.main"
            subtitle={`Новых в этом месяце: ${data.students.newThisMonth}`}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Кампании"
            value={data.campaigns.total}
            icon={<Campaign fontSize="large" />}
            color="warning.main"
            subtitle={`Потрачено: ${data.campaigns.totalSpent.toLocaleString()} ₽`}
          />
        </Grid>
      </Grid>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Финансы за месяц
              </Typography>
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <Box>
                  <Typography variant="h4" color="success.main">
                    {data.financials.monthly.netProfit.toLocaleString()} ₽
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Чистая прибыль
                  </Typography>
                </Box>
                <Box textAlign="right">
                  <Typography variant="h6">
                    {data.financials.monthly.grossRevenue.toLocaleString()} ₽
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Общий доход
                  </Typography>
                  <Typography variant="h6" color="error.main">
                    {data.financials.monthly.expenses.toLocaleString()} ₽
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Расходы
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Активность
              </Typography>
              <Box>
                <Typography variant="body1">
                  Активных курсов: {data.courses.active}
                </Typography>
                <Typography variant="body1">
                  Активных студентов: {data.students.active}
                </Typography>
                <Typography variant="body1">
                  Активных кампаний: {data.campaigns.active}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 