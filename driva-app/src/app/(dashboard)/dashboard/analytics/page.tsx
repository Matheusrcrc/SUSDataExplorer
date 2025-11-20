"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  TrendingUp,
  TrendingDown,
  Users,
  Mail,
  DollarSign,
  Target,
  ArrowUpRight,
  ArrowDownRight,
  Download,
} from "lucide-react";

const kpis = [
  {
    name: "Total de Leads",
    value: "2,345",
    change: "+12.5%",
    trend: "up",
    icon: Users,
  },
  {
    name: "Campanhas Ativas",
    value: "8",
    change: "+2",
    trend: "up",
    icon: Mail,
  },
  {
    name: "ROI Estimado",
    value: "R$ 125K",
    change: "+23.1%",
    trend: "up",
    icon: DollarSign,
  },
  {
    name: "Taxa de Conversão",
    value: "18.2%",
    change: "-2.3%",
    trend: "down",
    icon: Target,
  },
];

const funnelData = [
  { stage: "Novos Leads", count: 2345, percentage: 100 },
  { stage: "Contactados", count: 1876, percentage: 80 },
  { stage: "Qualificados", count: 1173, percentage: 50 },
  { stage: "Proposta", count: 469, percentage: 20 },
  { stage: "Negociação", count: 235, percentage: 10 },
  { stage: "Ganhos", count: 117, percentage: 5 },
];

const topOpportunities = [
  {
    company: "Tech Solutions Ltda",
    value: 125000,
    probability: 85,
    stage: "Negociação",
  },
  {
    company: "Inovação Digital S.A.",
    value: 98000,
    probability: 75,
    stage: "Proposta",
  },
  {
    company: "Sistemas Avançados",
    value: 87000,
    probability: 90,
    stage: "Negociação",
  },
  {
    company: "Cloud Services Pro",
    value: 76000,
    probability: 60,
    stage: "Qualificado",
  },
];

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Analytics</h1>
          <p className="text-muted-foreground">
            Acompanhe KPIs e performance das suas campanhas
          </p>
        </div>
        <Button>
          <Download className="h-4 w-4 mr-2" />
          Exportar Relatório
        </Button>
      </div>

      {/* KPIs Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {kpis.map((kpi) => (
          <Card key={kpi.name}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{kpi.name}</CardTitle>
              <kpi.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{kpi.value}</div>
              <p
                className={`text-xs flex items-center gap-1 ${
                  kpi.trend === "up" ? "text-green-600" : "text-red-600"
                }`}
              >
                {kpi.trend === "up" ? (
                  <ArrowUpRight className="h-3 w-3" />
                ) : (
                  <ArrowDownRight className="h-3 w-3" />
                )}
                {kpi.change} vs. mês anterior
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Funil de Conversão */}
        <Card>
          <CardHeader>
            <CardTitle>Funil de Conversão</CardTitle>
            <CardDescription>
              Visualização do pipeline de vendas
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {funnelData.map((stage, index) => (
                <div key={stage.stage} className="space-y-1">
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium">{stage.stage}</span>
                    <span className="text-muted-foreground">
                      {stage.count} ({stage.percentage}%)
                    </span>
                  </div>
                  <div className="w-full h-8 bg-muted rounded-md overflow-hidden relative">
                    <div
                      className={`h-full transition-all ${
                        index === 0
                          ? "bg-blue-500"
                          : index === 1
                          ? "bg-cyan-500"
                          : index === 2
                          ? "bg-teal-500"
                          : index === 3
                          ? "bg-green-500"
                          : index === 4
                          ? "bg-emerald-500"
                          : "bg-lime-500"
                      }`}
                      style={{ width: `${stage.percentage}%` }}
                    >
                      <div className="flex items-center justify-center h-full text-white text-xs font-medium">
                        {stage.count}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Performance por Canal */}
        <Card>
          <CardHeader>
            <CardTitle>Performance por Canal</CardTitle>
            <CardDescription>
              Efetividade de cada canal de comunicação
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center gap-2">
                    <Mail className="h-4 w-4" />
                    <span className="font-medium">Email</span>
                  </div>
                  <span className="text-muted-foreground">45% conversão</span>
                </div>
                <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500" style={{ width: "45%" }} />
                </div>
                <p className="text-xs text-muted-foreground">
                  1,234 enviados • 556 abertos • 234 respostas
                </p>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center gap-2">
                    <svg className="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0012.04 2m.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 012.41 5.83c0 4.54-3.7 8.23-8.24 8.23-1.48 0-2.93-.39-4.19-1.15l-.3-.17-3.12.82.83-3.04-.2-.32a8.188 8.188 0 01-1.26-4.38c.01-4.54 3.7-8.24 8.25-8.24M8.53 7.33c-.16 0-.43.06-.66.31-.22.25-.87.85-.87 2.07 0 1.22.89 2.39 1 2.56.14.17 1.76 2.67 4.25 3.73.59.27 1.05.42 1.41.53.59.19 1.13.16 1.56.1.48-.07 1.46-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.07-.1-.23-.16-.48-.27-.25-.14-1.47-.74-1.69-.82-.23-.08-.37-.12-.56.12-.16.25-.64.81-.78.97-.15.17-.29.19-.53.07-.26-.13-1.06-.39-2-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.02-.39.11-.5.11-.11.25-.29.37-.44.13-.14.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.11-.56-1.35-.77-1.84-.2-.48-.4-.42-.56-.43-.14 0-.3-.01-.46-.01z"/>
                    </svg>
                    <span className="font-medium">WhatsApp</span>
                  </div>
                  <span className="text-muted-foreground">62% conversão</span>
                </div>
                <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                  <div className="h-full bg-green-500" style={{ width: "62%" }} />
                </div>
                <p className="text-xs text-muted-foreground">
                  567 enviados • 489 abertos • 351 respostas
                </p>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center gap-2">
                    <svg className="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.79M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
                    </svg>
                    <span className="font-medium">LinkedIn</span>
                  </div>
                  <span className="text-muted-foreground">38% conversão</span>
                </div>
                <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                  <div className="h-full bg-blue-700" style={{ width: "38%" }} />
                </div>
                <p className="text-xs text-muted-foreground">
                  892 enviados • 445 abertos • 169 respostas
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Ranking de Oportunidades */}
      <Card>
        <CardHeader>
          <CardTitle>Ranking de Oportunidades</CardTitle>
          <CardDescription>
            Maiores oportunidades por valor estimado
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {topOpportunities.map((opp, index) => (
              <div
                key={opp.company}
                className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center font-bold text-primary">
                    #{index + 1}
                  </div>
                  <div>
                    <p className="font-medium">{opp.company}</p>
                    <p className="text-sm text-muted-foreground">
                      Estágio: {opp.stage}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold">
                    R$ {(opp.value / 1000).toFixed(0)}K
                  </p>
                  <p className="text-sm text-muted-foreground">
                    {opp.probability}% probabilidade
                  </p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
