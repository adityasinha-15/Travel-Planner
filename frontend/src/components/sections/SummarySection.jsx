import React from 'react'
import { FileText } from 'lucide-react'

const SummarySection = ({ summary }) => {
  return (
    <div className="card mb-8">
      <div className="flex items-center space-x-3 mb-4">
        <FileText className="h-5 w-5 text-primary-600" />
        <h2 className="text-xl font-semibold text-gray-900">Trip Summary</h2>
      </div>
      
      <div className="prose prose-gray max-w-none">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
            {summary}
          </p>
        </div>
      </div>
    </div>
  )
}

export default SummarySection
