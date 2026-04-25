import re

with open(r'E:\EE5215_LAB\clean_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract code blocks
# Lab 3 Code C
m_lab3 = re.search(r'Code C\s+(#include <stdio\.h>.*?return 0;\s*})', text, re.DOTALL)
lab3_code = m_lab3.group(1).strip() if m_lab3 else '// Code LAB 3 missing'

# Ex 1 Code
m_ex1 = re.search(r'Exercise 1:.*?Code C\s+(#include <stdio\.h>.*?return 0;\s*})', text, re.DOTALL)
ex1_code = m_ex1.group(1).strip() if m_ex1 else '// Code Ex 1 missing'

# Ex 2 Code
m_ex2 = re.search(r'Exercise 2:.*?Code C\s+(#include <stdio\.h>.*?return 0;\s*})', text, re.DOTALL)
ex2_code = m_ex2.group(1).strip() if m_ex2 else '// Code Ex 2 missing'

# Ex 3 Code
m_ex3 = re.search(r'Exercise 3:.*?Code C\s+(#include <stdio\.h>.*?return 0;\s*})', text, re.DOTALL)
ex3_code = m_ex3.group(1).strip() if m_ex3 else '// Code Ex 3 missing'

tex_content = r'''% =========================================================
% LAB 3  -  I2C Master Controller
% =========================================================
\newpage
\setcounter{section}{2}
\section{LAB3: DEVELOP SOFTWARE FOR NIOS II - PROCESSOR WITH SDRAM}

\subsection{Trình bày, vẽ sơ đồ mạch theo cách hiểu của học viên}

LAB3 tập trung vào thiết kế hệ thống SoC sử dụng vi xử lý Nios II kết hợp với bộ nhớ SDRAM để lưu trữ dữ liệu và mã lệnh. Sơ đồ mạch bên dưới thể hiện hệ thống được xây dựng trên Qsys/Platform Designer bao gồm bộ điều khiển SDRAM, JTAG UART, và các PIO I/O dùng để điều khiển LED/nút nhấn:

\begin{figure}[H]
    \centering
    \includegraphics[width=\linewidth]{images/fig_4_1.png}
    \caption{Sơ đồ kiến trúc kết nối hệ thống Nios II với SDRAM và PIO (LAB3)}
\end{figure}

\subsection{Sơ đồ dataflow với code software}

\begin{figure}[H]
    \centering
    \begin{tikzpicture}[node distance=0.8cm]
        \node[io]                               (start)  {Bắt đầu chương trình};
        \node[block, below=of start]            (initA)  {Tạo mảng A ngẫu nhiên\\(10 phần tử)};
        \node[block, below=of initA]            (copy)   {Sao chép mảng A\\sang mảng B};
        \node[block, below=of copy]             (sort)   {Sắp xếp mảng B\\(Bubble Sort)};
        \node[block, below=of sort]             (printA) {In mảng A (chưa sắp xếp)\\ra Console};
        \node[block, below=of printA]           (printB) {In mảng B (đã sắp xếp)\\ra Console};
        \node[io, below=of printB]              (end)    {Kết thúc};

        \draw[arrow] (start)  -- (initA);
        \draw[arrow] (initA)  -- (copy);
        \draw[arrow] (copy)   -- (sort);
        \draw[arrow] (sort)   -- (printA);
        \draw[arrow] (printA) -- (printB);
        \draw[arrow] (printB) -- (end);
    \end{tikzpicture}
    \caption{Sơ đồ dataflow thuật toán sắp xếp mảng SDRAM - LAB3}
\end{figure}

Đoạn mã C minh họa chương trình sắp xếp mảng:
\begin{lstlisting}[language=C, caption={C Source Code - LAB3}]
''' + lab3_code + r'''
\end{lstlisting}

\subsection{Báo cáo kết quả Quartus synthesis implementation, resource, $f_{max}$}
Kết quả synthesis Resource và $f_{max}$ của LAB3:

\begin{figure}[H]
    \centering
    \includegraphics[width=0.9\linewidth]{images/lab3_rtl_view_new_0.png}
    \caption{RTL View của LAB3 (Cập nhật)}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.9\linewidth]{images/lab3_resource.png}
    \caption{Tài nguyên sử dụng (Resource) của LAB3}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.9\linewidth]{images/lab3_fmax.png}
    \caption{Tần số hoạt động tối đa ($f_{max}$) của LAB3}
\end{figure}

\subsection{Hình ảnh chạy test code trên console}
Dưới đây là kết quả thực thi chương trình trên Nios II Console:
\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{images/lab3_console_0.png}
    \caption{Kết quả chạy test code trên console (LAB3)}
\end{figure}


% =========================================================
% LAB 4 & 5
% =========================================================
\newpage
\section{LAB4 \& 5: DEVELOP SOFTWARE FOR NIOS II - PROCESSOR WITH TIMER}

\subsection{Báo cáo kết quả Quartus synthesis implementation, resource, $f_{max}$}
Kết quả synthesis Resource và $f_{max}$ chung cho LAB 4 và LAB 5:

\begin{figure}[H]
    \centering
    \includegraphics[width=0.9\linewidth]{images/lab45_rtl_view_0.png}
    \caption{RTL View của LAB 4-5}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.9\linewidth]{images/lab45_resource_fmax_0.png}
    \caption{Tài nguyên sử dụng (Resource) của LAB 4-5}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.9\linewidth]{images/lab45_resource_fmax_1.png}
    \caption{Tần số hoạt động tối đa ($f_{max}$) của LAB 4-5}
\end{figure}

\subsection{Exercise 1}

Đoạn mã C cho Exercise 1:
\begin{lstlisting}[language=C, caption={C Source Code - LAB4\&5 Exercise 1}]
''' + ex1_code + r'''
\end{lstlisting}

\noindent\textbf{Video demo (Exercise 1):} \url{Ex1.mp4}

\subsection{Exercise 2}

Đoạn mã C cho Exercise 2:
\begin{lstlisting}[language=C, caption={C Source Code - LAB4\&5 Exercise 2}]
''' + ex2_code + r'''
\end{lstlisting}

\noindent\textbf{Video demo (Exercise 2):} \url{Ex2.mp4}

\subsection{Exercise 3}

Đoạn mã C cho Exercise 3:
\begin{lstlisting}[language=C, caption={C Source Code - LAB4\&5 Exercise 3}]
''' + ex3_code + r'''
\end{lstlisting}

\subsubsection{Kết quả thực thi}
\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\linewidth]{images/lab45_result_0.jpeg}
    \caption{Kết quả khi cả hai switch đều được thiết lập (Cả 2 switch lên 1)}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\linewidth]{images/lab45_result_1.jpeg}
    \caption{Kết quả khi cả hai switch đều không được thiết lập (Cả 2 switch về 0)}
\end{figure}

\noindent\textbf{Video demo Switch 1 set:} \url{Ex3_sw1_set.mp4}

\noindent\textbf{Video demo Switch 2 set:} \url{Ex3_sw2_set.mp4}

% =========================================================
% LAB 6
% =========================================================
\newpage
\section{LAB6: AVALON MEMORY-MAPPED (AVALON-MM) INTERFACE SPECIFICATION}

\subsection{Mục tiêu}
Thiết kế hệ thống Avalon-MM interconnection. Tập trung vào I/O của System Interconnect Fabric, thiết kế Slave Avalon-MM IP (System Interconnect Fabric sẽ tự động kết nối tất cả I/O từ Slave đến Master).

Thêm IP vào dự án Qsys trong Quartus. Sử dụng phần mềm Eclipse để lập trình dự án: Nhân ma trận (Matrix multiplication).

\subsection{Thực hành}
Thiết kế IP thực hiện nhân ma trận sử dụng giao thức Avalon Memory Map. NIOS II được kết nối và sử dụng như một công cụ quản lý dữ liệu, chuyển đầu vào tới và nhận đầu ra từ IP nhân ma trận.

\textbf{Các cổng I/O:}
\begin{itemize}
    \item \textbf{Inputs:} 2 ma trận với các phần tử là số 4-bit.
    \item \textbf{Outputs:} Ma trận chứa kết quả của phép nhân.
\end{itemize}

\textit{(Phần này giới thiệu cấu trúc của giao tiếp Avalon-MM theo yêu cầu của bài thực hành Lab 6.)}
'''

with open(r'E:\EE5215_LAB\chapters\ee5215_labs_3456.tex', 'w', encoding='utf-8') as f:
    f.write(tex_content)

print("Generated chapters/ee5215_labs_3456.tex successfully!")
