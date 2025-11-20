import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingUp, Users, Target, Mail, DollarSign, ArrowUpRight } from "lucide-react";

const stats = [
  {
    name: "Total de Leads",
    value: "2,345",
    change: "+12.5%",
    icon: Users,
    color: "text-blue-600",
    bgColor: "bg-blue-100",
  },
  {
    name: "Campanhas Ativas",
    value: "8",
    change: "+2",
    icon: Mail,
    color: "text-green-600",
    bgColor: "bg-green-100",
  },
  {
    name: "ROI Estimado",
    value: "R$ 125K",
    change: "+23.1%",
    icon: DollarSign,
    color: "text-purple-600",
    bgColor: "bg-purple-100",
  },
  {
    name: "Taxa de Conversão",
    value: "18.2%",
    change: "+4.3%",
    icon: TrendingUp,
    color: "text-orange-600",
    bgColor: "bg-orange-100",
  },
];

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Visão geral da sua inteligência comercial
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.name}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {stat.name}
              </CardTitle>
              <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                <stat.icon className={`h-4 w-4 ${stat.color}`} />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground flex items-center gap-1">
                <ArrowUpRight className="h-3 w-3 text-green-600" />
                {stat.change} em relação ao mês anterior
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Potencial de Mercado</CardTitle>
            <CardDescription>
              Mapeamento de oportunidades por região
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] flex items-center justify-center border-2 border-dashed rounded-lg">
              <p className="text-muted-foreground">
                Mapa de calor será renderizado aqui
              </p>
            </div>
          </CardContent>
        </Card>

        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Atividades Recentes</CardTitle>
            <CardDescription>
              Últimas interações e prospecções
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="flex items-start gap-4">
                  <div className="w-2 h-2 mt-2 rounded-full bg-primary" />
                  <div className="flex-1 space-y-1">
                    <p className="text-sm font-medium">
                      Novo lead adicionado
                    </p>
                    <p className="text-xs text-muted-foreground">
                      Empresa XYZ - Setor Tecnologia
                    </p>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Há {i}h
                  </p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Ações Rápidas</CardTitle>
          <CardDescription>
            Acesse as principais funcionalidades
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-4">
            <div className="flex flex-col items-center justify-center p-6 border rounded-lg hover:bg-accent cursor-pointer transition-colors">
              <Target className="h-8 w-8 mb-2 text-primary" />
              <p className="text-sm font-medium">Criar ICP</p>
            </div>
            <div className="flex flex-col items-center justify-center p-6 border rounded-lg hover:bg-accent cursor-pointer transition-colors">
              <Users className="h-8 w-8 mb-2 text-primary" />
              <p className="text-sm font-medium">Importar Leads</p>
            </div>
            <div className="flex flex-col items-center justify-center p-6 border rounded-lg hover:bg-accent cursor-pointer transition-colors">
              <Mail className="h-8 w-8 mb-2 text-primary" />
              <p className="text-sm font-medium">Nova Campanha</p>
            </div>
            <div className="flex flex-col items-center justify-center p-6 border rounded-lg hover:bg-accent cursor-pointer transition-colors">
              <TrendingUp className="h-8 w-8 mb-2 text-primary" />
              <p className="text-sm font-medium">Ver Analytics</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
