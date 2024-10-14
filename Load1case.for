		SUBROUTINE DLOAD(F,KSTEP,KINC,TIME,NOEL,NPT,LAYER,KSPT,
     1 COORDS,JLTYP,SNAME)
C
      INCLUDE 'ABA_PARAM.INC'
C
      DIMENSION TIME(2), COORDS (3)
      CHARACTER*80 SNAME
		real*8 P,t,L,F1
		z=coords(3)
		t=time(1)
		L=250
		A=L*4
		PZ=6505.45
C	*********************		
		if ((t.gt.0).and.(t.lt.0.11))then
			P=19655.03*t+PZ
		else if ((t.gt.0.11).and.(t.lt.0.401))then
			P=-14601.44*(t-0.11)+8667.5
		else if ((t.gt.0.401).and.(t.lt.0.601))then
			P=-6692.54*(t-0.401)+4396.58
		else if ((t.gt.0.601).and.(t.lt.0.801))then
			P=-795.9*(t-0.601)+2041.52
		else if ((t.gt.0.801).and.(t.lt.1))then
			P=16527.23*(t-0.801)+3200.52
		end if
C	*********************	
		if ((t.gt.0).and.(t.lt.0.05))then
			F1=-735591*t-45914.45
		else if ((t.gt.0.05).and.(t.lt.0.11))then
			F1=-1800096*(t-0.05)-82496
		else if ((t.gt.0.11).and.(t.lt.0.2))then
			F1=1198572*(t-0.11)-194075
		else if ((t.gt.0.2).and.(t.lt.0.3))then
			F1=432774*(t-0.2)-86203
		else if ((t.gt.0.3).and.(t.lt.0.4))then
			F1=136957*(t-0.3)-42926
		else if ((t.gt.0.4).and.(t.lt.0.86))then
			F1=13298.15*(t-0.4)-29230.4
		else 
			F1=-162865.71*(t-0.86)-23113.25
		end if
C	*********************		
      if ((Z.gt.(P-L)).and.(Z.lt.(P+L)))then
		F=-F1/A
	  else
		F=0
	  end if
      RETURN
      END