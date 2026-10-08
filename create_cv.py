from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('CVSans','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('CVSansBold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('CVSans',normal='CVSans',bold='CVSansBold',italic='CVSans',boldItalic='CVSansBold')
out=Path(__file__).parent/'assets/Matteo-Paolini-CV.pdf'
styles={
'name':ParagraphStyle('name',fontName='CVSansBold',fontSize=25,leading=29,spaceAfter=5),
'lead':ParagraphStyle('lead',fontName='CVSans',fontSize=10,leading=14,spaceAfter=6),
'body':ParagraphStyle('body',fontName='CVSans',fontSize=9,leading=12,spaceAfter=5),
'head':ParagraphStyle('head',fontName='CVSansBold',fontSize=10,leading=14,spaceBefore=12,spaceAfter=6,textColor=colors.HexColor('#245b9e')),
'item':ParagraphStyle('item',fontName='CVSansBold',fontSize=9.5,leading=13,spaceBefore=4,spaceAfter=3)}
story=[]
def p(text,style='body'):story.append(Paragraph(text,styles[style]))
p('Matteo Paolini','name')
p('Mechanical Engineering M.Sc. student | Mechatronics &amp; Robotics','lead')
p('Brussels / Italy · Open to relocation<br/><a href="mailto:paolini134@gmail.com">paolini134@gmail.com</a> · <a href="https://matpaol.github.io">matpaol.github.io</a> · <a href="https://github.com/matpaol">github.com/matpaol</a> · <a href="https://linkedin.com/in/matpaolini">linkedin.com/in/matpaolini</a>','body')
p('RESEARCH EXPERIENCE','head')
p('Research Intern - Royal Military Academy, Brussels | 2026 - Present','item')
p('DREAM project · Work in progress. Research on Physical AI for robotic manipulation, with a focus on reinforcement learning, hierarchical RL and sim-to-real transfer. Developing reproducible MuJoCo scenes, physics diagnostics and Gymnasium-based learning experiments; exploring counterfactual reasoning for physical interactions in cluttered scenes.')
p('EDUCATION','head')
p('M.Sc. Mechanical Engineering - Mechatronics | UNIVPM | 2024 - Present','item')
p('Erasmus coursework at Université Libre de Bruxelles (ULB) and Vrije Universiteit Brussel (VUB), 2025-2026. Robotics, control, industrial automation and data science.')
p('B.Sc. Mechanical Engineering | UNIVPM | 2021 - 2024','item')
p('Thesis: motion planning for redundant robots (TIAGo). Implemented and compared RRT and RRT* for collision-free pick-and-place trajectories.')
p('SELECTED ENGINEERING PROJECTS','head')
p('Dual-arm Object Handover | Individual project | 2025-2026','item')
p('Developed the complete Drake/OMPL simulation pipeline for two Franka Panda arms: workspace analysis, inverse kinematics, motion planning, grasp ownership and task coordination. Demonstrated a 13-state pick-handover-place sequence; one nominal simulated run completed in approximately 20 seconds with 9.1 mm placement error.')
p('Tentacle Robotic Gripper | Team project | 2025','item')
p('My contribution: hyperelastic FEM of the pneumatic silicone actuator, casting-mold CAD and 3D-printed tooling. Integrated by the team into a soft gripper and two-degree-of-freedom arm; public build guide and prototype video.')
p('Apple Watch Case - Manufacturing Study | Academic project | 2025','item')
p('Reconstructed case geometry and prepared manufacturing drawings. Developed a proposed high-volume production workflow, with machining calculations, tool-life estimates and sheet nesting. Material and geometry assumptions support an academic process-design study.')
p('vacUUUm - Cordless Vacuum Design | Team project | 2025','item')
p('Connected user research and QFD to functional decomposition and product architecture. Worked on Siemens NX CAD, assembly layouts and technical drawings for a cordless vacuum and charging station.')
p('CubeSat 1U Structure | Academic project | 2025','item')
p('Studied a hybrid chassis with composite panels and aluminium rails using ANSYS/ACP. Defined a symmetric 16-ply, 2 mm laminate and investigated structural design and multi-material integration.')
p('SKILLS','head')
p('<b>Robotics &amp; software:</b> Python, MuJoCo, Gymnasium, Drake, OMPL, MATLAB/Simulink.<br/><b>Engineering:</b> Siemens NX, ANSYS Workbench/ACP, FEM, hyperelastic modelling, mold design, technical drawings, FDM 3D printing.<br/><b>Materials:</b> metallographic sample preparation, microscopy and Vickers hardness testing.<br/><b>Languages:</b> Italian (native), English (C1).')
SimpleDocTemplate(str(out),pagesize=(595.28,841.89),rightMargin=40,leftMargin=40,topMargin=34,bottomMargin=30,title='Matteo Paolini - Curriculum Vitae',author='Matteo Paolini').build(story)
