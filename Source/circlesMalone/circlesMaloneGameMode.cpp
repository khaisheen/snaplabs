// Copyright 1998-2019 Epic Games, Inc. All Rights Reserved.

#include "circlesMaloneGameMode.h"
#include "circlesMaloneCharacter.h"

AcirclesMaloneGameMode::AcirclesMaloneGameMode()
{
	// Set default pawn class to our character
	DefaultPawnClass = AcirclesMaloneCharacter::StaticClass();	
}
