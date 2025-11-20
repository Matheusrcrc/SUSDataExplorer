"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Plus, Mail, MessageSquare, Linkedin, Play, Pause, Sparkles } from "lucide-react";

const mockCampaigns = [
  {
    id: "1",
    name: "Outreach Tech Companies Q1",
    status: "ACTIVE",
    channels: ["EMAIL", "LINKEDIN"],
    leads: 245,
    sent: 180,
    opened: 95,
    replied: 23,
    startDate: "2024-01-15",
  },
  {
    id: "2",
    name: "WhatsApp Follow-up",
    status: "PAUSED",
    channels: ["WHATSAPP"],
    leads: 120,
    sent: 45,
    opened: 30,
    replied: 8,
    startDate: "2024-01-20",
  },
];

export default function ProspectingPage() {
  const [showCopilot, setShowCopilot] = useState(false);
  const [copilotPrompt, setCopilotPrompt] = useState("");
  const [copilotResponse, setCopilotResponse] = useState("");

  const handleAskCopilot = () => {
    // Simulação de resposta da IA
    setCopilotResponse(`Com base na sua solicitação sobre "${copilotPrompt}", recomendo:

1. **Melhor horário para contato**: Terças e quartas-feiras, entre 9h-11h e 14h-16h
2. **Abordagem sugerida**:
   - Primeira mensagem: Apresentação + valor agregado
   - Follow-up 1 (3 dias depois): Case de sucesso relevante
   - Follow-up 2 (5 dias depois): Proposta de reunião rápida
3. **Script sugerido para email**:
   "Olá [Nome], percebi que sua empresa [Empresa] atua em [Setor]. Temos ajudado empresas similares a [benefício específico]. Posso compartilhar um case rápido em uma call de 15 minutos?"

Deseja que eu gere templates personalizados para cada canal?`);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            Workflow de Prospecção
          </h1>
          <p className="text-muted-foreground">
            Automatize cadências multicanal e acompanhe resultados
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => setShowCopilot(!showCopilot)}>
            <Sparkles className="h-4 w-4 mr-2" />
            IA Copilot
          </Button>
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            Nova Campanha
          </Button>
        </div>
      </div>

      {/* IA Copilot */}
      {showCopilot && (
        <Card className="bg-gradient-to-br from-purple-50 to-blue-50 border-purple-200">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-purple-600" />
              IA Copilot - Assistente de Prospecção
            </CardTitle>
            <CardDescription>
              Obtenha sugestões de abordagem, scripts e melhores horários para contato
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="copilot-prompt">O que você gostaria de saber?</Label>
              <Input
                id="copilot-prompt"
                placeholder="Ex: Qual o melhor horário para prospectar empresas de tecnologia?"
                value={copilotPrompt}
                onChange={(e) => setCopilotPrompt(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    handleAskCopilot();
                  }
                }}
              />
              <Button onClick={handleAskCopilot} className="mt-2">
                Perguntar à IA
              </Button>
            </div>

            {copilotResponse && (
              <div className="mt-4 p-4 bg-white rounded-lg border">
                <p className="text-sm font-medium mb-2">Resposta da IA:</p>
                <div className="text-sm whitespace-pre-line text-muted-foreground">
                  {copilotResponse}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Campanhas Ativas */}
      <div className="grid gap-6 md:grid-cols-2">
        {mockCampaigns.map((campaign) => (
          <Card key={campaign.id}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle>{campaign.name}</CardTitle>
                  <CardDescription>
                    Iniciada em {new Date(campaign.startDate).toLocaleDateString("pt-BR")}
                  </CardDescription>
                </div>
                <span
                  className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                    campaign.status === "ACTIVE"
                      ? "bg-green-100 text-green-800"
                      : "bg-yellow-100 text-yellow-800"
                  }`}
                >
                  {campaign.status}
                </span>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex gap-2">
                {campaign.channels.map((channel) => (
                  <div
                    key={channel}
                    className="flex items-center gap-1 px-2 py-1 bg-primary/10 rounded-md text-xs"
                  >
                    {channel === "EMAIL" && <Mail className="h-3 w-3" />}
                    {channel === "WHATSAPP" && <MessageSquare className="h-3 w-3" />}
                    {channel === "LINKEDIN" && <Linkedin className="h-3 w-3" />}
                    {channel}
                  </div>
                ))}
              </div>

              <div className="grid grid-cols-4 gap-4 text-center">
                <div>
                  <p className="text-2xl font-bold">{campaign.leads}</p>
                  <p className="text-xs text-muted-foreground">Leads</p>
                </div>
                <div>
                  <p className="text-2xl font-bold">{campaign.sent}</p>
                  <p className="text-xs text-muted-foreground">Enviados</p>
                </div>
                <div>
                  <p className="text-2xl font-bold">{campaign.opened}</p>
                  <p className="text-xs text-muted-foreground">Abertos</p>
                </div>
                <div>
                  <p className="text-2xl font-bold">{campaign.replied}</p>
                  <p className="text-xs text-muted-foreground">Respostas</p>
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Taxa de Abertura</span>
                  <span className="font-medium">
                    {((campaign.opened / campaign.sent) * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                  <div
                    className="h-full bg-primary"
                    style={{ width: `${(campaign.opened / campaign.sent) * 100}%` }}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Taxa de Resposta</span>
                  <span className="font-medium">
                    {((campaign.replied / campaign.sent) * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                  <div
                    className="h-full bg-green-500"
                    style={{ width: `${(campaign.replied / campaign.sent) * 100}%` }}
                  />
                </div>
              </div>

              <div className="flex gap-2">
                <Button variant="outline" size="sm" className="flex-1">
                  {campaign.status === "ACTIVE" ? (
                    <>
                      <Pause className="h-4 w-4 mr-2" />
                      Pausar
                    </>
                  ) : (
                    <>
                      <Play className="h-4 w-4 mr-2" />
                      Retomar
                    </>
                  )}
                </Button>
                <Button variant="outline" size="sm" className="flex-1">
                  Ver Detalhes
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Configurar Nova Cadência */}
      <Card>
        <CardHeader>
          <CardTitle>Configurar Cadência de Prospecção</CardTitle>
          <CardDescription>
            Crie sequências automatizadas multicanal
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="campaign-name">Nome da Campanha</Label>
                <Input
                  id="campaign-name"
                  placeholder="Ex: Outreach Tech Q1 2024"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="campaign-leads">Selecionar Leads</Label>
                <Input id="campaign-leads" placeholder="Escolher lista..." />
              </div>
            </div>

            <div className="space-y-2">
              <Label>Canais de Comunicação</Label>
              <div className="flex gap-4">
                <label className="flex items-center gap-2">
                  <input type="checkbox" defaultChecked />
                  <Mail className="h-4 w-4" />
                  Email
                </label>
                <label className="flex items-center gap-2">
                  <input type="checkbox" />
                  <MessageSquare className="h-4 w-4" />
                  WhatsApp
                </label>
                <label className="flex items-center gap-2">
                  <input type="checkbox" defaultChecked />
                  <Linkedin className="h-4 w-4" />
                  LinkedIn
                </label>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="email-template">Template de Email</Label>
              <textarea
                id="email-template"
                className="w-full min-h-[100px] p-3 border rounded-md"
                placeholder="Olá [Nome],&#10;&#10;Percebi que sua empresa..."
              />
            </div>

            <div className="flex gap-2">
              <Button>Criar Campanha</Button>
              <Button variant="outline">Salvar Rascunho</Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
