"use client"

import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, LineChart, Line, PieChart, Pie, Cell } from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card"
import { Loader2 } from "lucide-react"
import { logger } from '@/utils/logger'

type GraphSpec = {
  type: string
  x: string
  y: string
  title: string
  dataFilter: Record<string, string>
  xAxis: string
  yAxis: string
  layout: Record<string, number>
}

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#0088fe']

export default function GraphSection() {
  const [graphs, setGraphs] = useState<GraphSpec[]>([])
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  
  // Show 3 placeholder boxes initially
  const placeholderGraphs = Array(3).fill(null)

  useEffect(() => {
    const fetchInitialGraphs = async () => {
      try {
        console.log("Starting fetch...");
        setLoading(true);
        
        const response = await fetch('http://localhost:8000/initial-graphs');
        const result = await response.json();
        console.log("Received data:", result);

        if (result.graphs && result.data) {
          setGraphs(result.graphs);
          setData(result.data);
          console.log("Set graphs:", result.graphs.length, "and data:", result.data.length);
        }
      } catch (error) {
        console.error("Fetch error:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchInitialGraphs();
  }, []);

  useEffect(() => {
    const handleGraphUpdate = (event: CustomEvent) => {
      logger.log(`🔄 Received graph update event: ${JSON.stringify(event.detail)}`);
      if (event.detail.append) {
        setGraphs(prev => [...prev, ...event.detail.graphs]);
        setData(event.detail.data);
      } else {
        setGraphs(event.detail.graphs);
        setData(event.detail.data);
      }
    }

    window.addEventListener('updateGraphs', handleGraphUpdate as EventListener);
    return () => {
      window.removeEventListener('updateGraphs', handleGraphUpdate as EventListener);
    }
  }, []);

  const renderGraph = (graph: any, data: any[]) => {
    const filteredData = data.filter(item => 
      Object.entries(graph.dataFilter).every(([key, value]) => 
        item[key] === value
      )
    );

    if (graph.type === 'bar') {
      return (
        <BarChart width={400} height={250} data={filteredData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={graph.xAxis} />
          <YAxis 
            dataKey={graph.yAxis} 
            tickFormatter={(value) => value.toLocaleString()} 
          />
          <Tooltip />
          <Bar dataKey={graph.yAxis} fill="#8884d8" />
        </BarChart>
      );
    }

    if (graph.type === 'pie') {
      return (
        <PieChart width={400} height={250}>
          <Pie
            data={filteredData}
            dataKey={graph.values}
            nameKey={graph.labels}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={80}
          >
            {filteredData.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      );
    }
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
      {loading ? (
        placeholderGraphs.map((_, index) => (
          <motion.div key={`placeholder-${index}`}>
            <Card className="w-full h-[350px] flex items-center justify-center">
              <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
            </Card>
          </motion.div>
        ))
      ) : (
        graphs
          .filter(graph => ['bar', 'line', 'pie'].includes(graph.type.toLowerCase()))
          .map((graph, index) => (
            <motion.div key={index} className="w-full">
              <Card className="h-[350px]">
                <CardHeader>
                  <CardTitle className="text-center text-sm font-medium">{graph.title}</CardTitle>
                </CardHeader>
                <CardContent className="flex items-center justify-center">
                  {data.length > 0 && renderGraph(graph, data)}
                </CardContent>
              </Card>
            </motion.div>
          ))
      )}
    </div>
  )
}

