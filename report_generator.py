"""
Interview Report Generator
Analyzes answers, provides feedback, and generates PDF report
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import os

class InterviewReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ))
    
    def analyze_answer(self, question, answer, category):
        """Analyze a single answer and provide feedback"""
        answer_length = len(answer.split())
        
        # Basic scoring
        if answer_length < 10:
            score = 3
            feedback = "Answer is too brief. Provide more detailed explanations."
        elif answer_length < 30:
            score = 5
            feedback = "Good start, but could be more comprehensive."
        elif answer_length < 60:
            score = 7
            feedback = "Well-explained answer with good detail."
        else:
            score = 9
            feedback = "Excellent, comprehensive answer!"
        
        # Category-specific feedback
        if category.lower() == 'technical':
            if any(word in answer.lower() for word in ['example', 'for instance', 'such as']):
                score += 1
                feedback += " Great use of examples!"
        else:  # Behavioral
            if any(word in answer.lower() for word in ['i', 'my', 'we', 'our']):
                score = min(10, score + 1)
                feedback += " Good use of personal experience!"
        
        return min(10, score), feedback
    
    def calculate_overall_score(self, question_scores):
        """Calculate overall performance score"""
        if not question_scores:
            return 0, "No answers provided"
        
        avg_score = sum(question_scores) / len(question_scores)
        
        if avg_score >= 9:
            grade = "A+"
            performance = "Excellent"
        elif avg_score >= 8:
            grade = "A"
            performance = "Very Good"
        elif avg_score >= 7:
            grade = "B+"
            performance = "Good"
        elif avg_score >= 6:
            grade = "B"
            performance = "Above Average"
        elif avg_score >= 5:
            grade = "C"
            performance = "Average"
        else:
            grade = "D"
            performance = "Needs Improvement"
        
        return avg_score, grade, performance
    
    def generate_improvement_suggestions(self, category, avg_score, answers):
        """Generate personalized improvement suggestions"""
        suggestions = []
        
        # General suggestions based on score
        if avg_score < 6:
            suggestions.append("Practice answering questions with more detail and structure")
            suggestions.append("Research common interview questions in your field")
        
        # Category-specific suggestions
        if category.lower() == 'technical':
            suggestions.extend([
                "Study fundamental concepts and data structures",
                "Practice coding problems on platforms like LeetCode or HackerRank",
                "Work on real-world projects to gain practical experience",
                "Learn to explain technical concepts in simple terms",
                "Stay updated with latest technologies and best practices"
            ])
        else:  # Behavioral
            suggestions.extend([
                "Use the STAR method (Situation, Task, Action, Result)",
                "Prepare specific examples from your experience",
                "Practice storytelling to make answers more engaging",
                "Focus on quantifiable achievements",
                "Show self-awareness and learning from experiences"
            ])
        
        # Check answer lengths
        avg_length = sum(len(a.split()) for a in answers) / len(answers) if answers else 0
        if avg_length < 30:
            suggestions.append("Provide more detailed and comprehensive answers")
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def generate_pdf_report(self, session_data, output_path):
        """Generate comprehensive PDF report"""
        
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                               topMargin=0.5*inch, bottomMargin=0.5*inch,
                               leftMargin=0.75*inch, rightMargin=0.75*inch)
        
        story = []
        
        # Title
        title = Paragraph("AI Interview Performance Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Candidate Info
        info_data = [
            ['Candidate:', session_data.get('username', 'N/A')],
            ['Role:', session_data.get('role', 'N/A')],
            ['Category:', session_data.get('category', 'N/A')],
            ['Date:', datetime.now().strftime('%B %d, %Y')],
            ['Duration:', f"{session_data.get('duration', 0)} minutes"]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Overall Performance
        avg_score, grade, performance = self.calculate_overall_score(session_data.get('scores', []))
        
        perf_title = Paragraph("Overall Performance", self.styles['CustomSubtitle'])
        story.append(perf_title)
        
        perf_data = [
            ['Average Score:', f"{avg_score:.1f}/10"],
            ['Grade:', grade],
            ['Performance Level:', performance],
            ['Questions Answered:', f"{len(session_data.get('answers', []))}/{session_data.get('total_questions', 0)}"]
        ]
        
        perf_table = Table(perf_data, colWidths=[2.5*inch, 3.5*inch])
        perf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f4f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        story.append(perf_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Monitoring Metrics
        if session_data.get('tracking_data'):
            tracking = session_data['tracking_data']
            
            metrics_title = Paragraph("Monitoring Metrics", self.styles['CustomSubtitle'])
            story.append(metrics_title)
            
            metrics_data = [
                ['Metric', 'Score', 'Status'],
                ['Posture Score', f"{tracking.get('posture_score', 0):.0f}%", 
                 'Good' if tracking.get('posture_score', 0) > 70 else 'Needs Improvement'],
                ['Eye Contact', f"{tracking.get('eye_contact', 0):.0f}%",
                 'Good' if tracking.get('eye_contact', 0) > 70 else 'Needs Improvement'],
                ['Focus Level', f"{tracking.get('focus', 0):.0f}%",
                 'Good' if tracking.get('focus', 0) > 70 else 'Needs Improvement'],
                ['Tab Switches', str(tracking.get('tab_switches', 0)),
                 'Good' if tracking.get('tab_switches', 0) == 0 else 'Warning']
            ]
            
            metrics_table = Table(metrics_data, colWidths=[2*inch, 2*inch, 2*inch])
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
            ]))
            story.append(metrics_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Question-by-Question Analysis
        story.append(PageBreak())
        
        qa_title = Paragraph("Question-by-Question Analysis", self.styles['CustomSubtitle'])
        story.append(qa_title)
        story.append(Spacer(1, 0.2*inch))
        
        for i, (question, answer) in enumerate(zip(session_data.get('questions', []), 
                                                    session_data.get('answers', [])), 1):
            # Question
            q_text = Paragraph(f"<b>Q{i}:</b> {question}", self.styles['Normal'])
            story.append(q_text)
            story.append(Spacer(1, 0.1*inch))
            
            # Answer
            a_text = Paragraph(f"<b>Answer:</b> {answer}", self.styles['Normal'])
            story.append(a_text)
            story.append(Spacer(1, 0.1*inch))
            
            # Score and Feedback
            score, feedback = self.analyze_answer(question, answer, session_data.get('category', 'Technical'))
            
            score_data = [
                ['Score:', f"{score}/10"],
                ['Feedback:', feedback]
            ]
            
            score_table = Table(score_data, colWidths=[1*inch, 5*inch])
            score_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            story.append(score_table)
            story.append(Spacer(1, 0.2*inch))
        
        # Improvement Suggestions
        story.append(PageBreak())
        
        improve_title = Paragraph("Areas for Improvement", self.styles['CustomSubtitle'])
        story.append(improve_title)
        story.append(Spacer(1, 0.2*inch))
        
        suggestions = self.generate_improvement_suggestions(
            session_data.get('category', 'Technical'),
            avg_score,
            session_data.get('answers', [])
        )
        
        for i, suggestion in enumerate(suggestions, 1):
            sug_text = Paragraph(f"{i}. {suggestion}", self.styles['Normal'])
            story.append(sug_text)
            story.append(Spacer(1, 0.1*inch))
        
        # Build PDF
        doc.build(story)
        
        return output_path

# Export
if __name__ == '__main__':
    # Test
    generator = InterviewReportGenerator()
    print("Report generator ready!")
