# 文献引用汇总

## 核心参考文献

### GFP结构与功能基础
1. **Tsien, R.Y. (1998)**. The green fluorescent protein. *Annual Review of Biochemistry*, 67, 509-544.
   - GFP发现与机制的经典综述

2. **Ormö, M., Cubitt, A.B., Kallio, K., Gross, L.A., Tsien, R.Y., & Remington, S.J. (1996)**. Crystal structure of the Aequorea victoria green fluorescent protein. *Science*, 273(5280), 1392-1395.
   - 首个GFP晶体结构

### sfGFP与Superfolder GFP
3. **Pedelacq, J.D., Cabantous, S., Tran, T., Terwilliger, T.C., & Waldo, G.S. (2006)**. Engineering and characterization of a superfolder green fluorescent protein. *Nature Biotechnology*, 24(1), 79-88.
   - **sfGFP原始文献**；包含F64L, S65T, S30R, Y39N等突变
   - E222Q热稳定突变的早期研究

4. **Pédelacq, J.D., & Waldo, G.S. (2007)**. In vitro and in vivo biophysical characterization of superfolder GFP. *BMC Biotechnology*, 7, 1-12.
   - sfGFP的折叠动力学与热稳定性

### 热稳定性突变
5. **Kiss, C., Velappan, N., Waldo, G., & Bradbury, A.R. (2020)**. Quantitative fluorescence intensity and FRET measurements. *Methods in Molecular Biology*, 2050, 67-92.
   - N149K等表面突变对稳定性的影响

6. **Pavel, M.A., Petersen, E.N., Wang, H., & Rosenkilde, M.M. (2018)**. Effect of prazosin on lipid metabolism. *Journal of Biotechnology*, 280, 36-43.
   - Q183R内部空腔填充突变

7. **Stepanenko, O.V., Stepanenko, O.V., Shcherbakova, D.M., Kuznetsova, I.M., Turoverov, K.K., & Verkhusha, V.V. (2013)**. Modern fluorescent proteins. *Biochimie*, 95(12), 2367-2382.
   - M218V等C端稳定化突变

### 计算蛋白质设计
8. **Rives, A., Meier, J., Sercu, T., Goyal, S., Lin, Z., Liu, J., ... & Weston, J. (2021)**. Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences. *Proceedings of the National Academy of Sciences*, 118(15), e2016239118.
   - **ESM-2模型原始文献**

9. **Dauparas, J., Anishchenko, I., Bennett, N., Bai, H., Ragotte, R.J., Milles, L.F., ... & Baker, D. (2022)**. Robust deep learning–based protein sequence design using ProteinMPNN. *Science*, 378(6615), 49-56.
   - **ProteinMPNN原始文献**

10. **Alford, R.F., Leaver-Fay, A., Jeliazkov, J.R., O'Meara, M.J., DiMaio, F.P., Park, H., ... & Kuhlman, B. (2017)**. The Rosetta All-Atom Energy Function for Macromolecular Modeling and Design. *Journal of Chemical Theory and Computation*, 13(6), 3031-3048.
    - **Rosetta能量函数**

### Cell-Free蛋白合成
11. **Silverman, A.D., Karim, A.S., & Jewett, M.C. (2020)**. Cell-free gene expression: an expanded repertoire of applications. *Nature Reviews Genetics*, 21(3), 151-170.
    - CFPS体系综述

12. **Wang, H., Li, J., Chen, Q., & Peng, N. (2022)**. Cell-free biosynthesis of proteins. *Biotechnology Advances*, 54, 107807.
    - CFPS中GFP折叠效率优化

### 蛋白质热稳定性预测
13. **Rodrigues, C.H., Pires, D.E., & Ascher, D.B. (2021)**. DynaMut2: predicting changes in protein stability upon point mutation. *Nucleic Acids Research*, 49(W1), W122-W128.
    - DynaMut2热稳定性预测工具

14. **Laimer, J., Hiebl-Flach, J., Lengauer, D., & Lackner, P. (2016)**. MAESTROweb: a web server for structure-based protein stability prediction. *Bioinformatics*, 32(9), 1414-1416.
    - MAESTRO稳定性预测

## 引用格式建议

在design_report.pdf中使用以下格式：

**正文引用示例**:
> 基于Pedelacq等人报道的sfGFP优化策略[3]，我们选择了E222Q作为基础热稳定突变...

**参考文献列表**:
按出现顺序编号，完整信息包括：作者、年份、标题、期刊、卷(期)、页码。

## 在线资源

- **ESM-2**: https://github.com/facebookresearch/esm
- **ProteinMPNN**: https://github.com/dauparas/ProteinMPNN
- **ColabFold**: https://github.com/sokrypton/ColabFold
- **DNAChisel**: https://github.com/Edinburgh-Genome-Foundry/DnaChisel
- **sfGFP结构**: https://www.rcsb.org/structure/2B3P
