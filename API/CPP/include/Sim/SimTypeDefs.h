//////////////////////////////////////////////////////////////////////////////
//
// Copyright 2026 Autodesk, Inc. All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software.
//
//////////////////////////////////////////////////////////////////////////////

#pragma once

namespace adsk { namespace sim {

/// !!!!! Warning !!!!!
/// ! This is hidden and not officially supported
/// !!!!! Warning !!!!!
/// 
/// Simulation constraint types.
enum ConstraintTypes
{
    /// Unknown constraint type.
    UnknownConstraintType,
    /// Fixed constraint type.
    FixedConstraintType,
    /// Frictionless constraint type.
    FrictionlessConstraintType,
    /// Prescribed displacement constraint type.
    PrescribedDisplacementConstraintType,
    /// Pin constraint type.
    PinConstraintType,
    /// Remote constraint type.
    RemoteConstraintType
};

/// !!!!! Warning !!!!!
/// ! This is hidden and not officially supported
/// !!!!! Warning !!!!!
/// 
/// Mesh element order types.
enum ElementOrderTypes
{
    /// Unknown element order type.
    UnknownElementOrderType,
    /// Linear element order type.
    LinearElementOrderType,
    /// Parabolic (quadratic) element order type.
    ParabolicElementOrderType
};

/// !!!!! Warning !!!!!
/// ! This is hidden and not officially supported
/// !!!!! Warning !!!!!
/// 
/// Determination of the average element size.
enum ElementSizeDeterminationTypes
{
    /// Unknown element size determination type.
    UnknownElementSizeDeterminationType,
    /// Average element size as a proportion of the model size.
    SizeByModelElementSizeDeterminationType,
    /// An absolute value for the average element size.
    AbsoluteElementSizeDeterminationType
};

/// !!!!! Warning !!!!!
/// ! This is hidden and not officially supported
/// !!!!! Warning !!!!!
/// 
/// Load direction types.
enum LoadDirectionTypes
{
    /// Unknown load direction type.
    UnknownLoadDirectionType,
    /// Load direction type default.
    DefaultLoadDirectionType,
    /// Load direction type cartesian.
    CartesianLoadDirectionType,
    /// Load direction type angles.
    AnglesLoadDirectionType,
    /// Load direction type reference.
    ReferenceLoadDirectionType
};

/// !!!!! Warning !!!!!
/// ! This is hidden and not officially supported
/// !!!!! Warning !!!!!
/// 
/// Simulation study types.
enum StudyTypes
{
    /// Unknown study type.
    UnknownStudyType,
    /// Structural linear static stress simulation study type.
    LinearStaticStressStudyType,
    /// Structural nonlinear static stress simulation study type.
    NonLinearStaticStressStudyType,
    /// Structural dynamic event simulation study type.
    DynamicEventSimulationStudyType
};

}// namespace sim
}// namespace adsk
