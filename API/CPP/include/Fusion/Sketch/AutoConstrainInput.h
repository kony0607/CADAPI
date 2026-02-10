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
#include "../../Core/Base.h"
#include "../FusionTypeDefs.h"
#include <string>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef FUSIONXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_FUSION_AUTOCONSTRAININPUT_CPP__
# define ADSK_FUSION_AUTOCONSTRAININPUT_API XI_EXPORT
# else
# define ADSK_FUSION_AUTOCONSTRAININPUT_API
# endif
#else
# define ADSK_FUSION_AUTOCONSTRAININPUT_API XI_IMPORT
#endif

namespace adsk { namespace fusion {
    class Sketch;
    class SketchPoint;
}}

namespace adsk { namespace fusion {

/// !!!!! Warning !!!!!
/// ! This is in preview state; please see the help for more info
/// !!!!! Warning !!!!!
/// 
/// The AutoConstrainInput object is used to define the various options when adding dimension
/// and geometric constraints to help constrain a sketch.
class AutoConstrainInput : public core::Base {
public:

    /// Gets and sets an optional datum point that the dimensions will be based on. This defaults to null,
    /// which indicates there is no datum point specified. When no datum point is provided, AutoConstrain
    /// will automatically select an appropriate datum based on the sketch content and geometry.
    core::Ptr<SketchPoint> datumPoint() const;
    bool datumPoint(const core::Ptr<SketchPoint>& value);

    /// Returns the Sketch this object is associated with and where the dimension and geometric constraints
    /// will be added when the autoConstrain method is called. This property is read-only and is set when
    /// the input object is created by the sketch's createAutoConstrainInput method.
    core::Ptr<Sketch> parentSketch() const;

    /// !!!!! Warning !!!!!
    /// ! This is hidden and not officially supported
    /// !!!!! Warning !!!!!
    /// 
    /// Specifies the internal recipe of how the sketch should be solved. This property is intended for
    /// internal use and advanced scenarios. The available recipe values are implementation-specific
    /// and may change between versions. Most users should rely on the default approach
    /// by leaving this property unset (null or empty string).
    std::string recipe() const;
    bool recipe(const std::string& value);

    ADSK_FUSION_AUTOCONSTRAININPUT_API static const char* classType();
    ADSK_FUSION_AUTOCONSTRAININPUT_API const char* objectType() const override;
    ADSK_FUSION_AUTOCONSTRAININPUT_API void* queryInterface(const char* id) const override;
    ADSK_FUSION_AUTOCONSTRAININPUT_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual SketchPoint* datumPoint_raw() const = 0;
    virtual bool datumPoint_raw(SketchPoint* value) = 0;
    virtual Sketch* parentSketch_raw() const = 0;
    virtual char* recipe_raw() const = 0;
    virtual bool recipe_raw(const char* value) = 0;
};

// Inline wrappers

inline core::Ptr<SketchPoint> AutoConstrainInput::datumPoint() const
{
    core::Ptr<SketchPoint> res = datumPoint_raw();
    return res;
}

inline bool AutoConstrainInput::datumPoint(const core::Ptr<SketchPoint>& value)
{
    return datumPoint_raw(value.get());
}

inline core::Ptr<Sketch> AutoConstrainInput::parentSketch() const
{
    core::Ptr<Sketch> res = parentSketch_raw();
    return res;
}

inline std::string AutoConstrainInput::recipe() const
{
    std::string res;

    char* p= recipe_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline bool AutoConstrainInput::recipe(const std::string& value)
{
    return recipe_raw(value.c_str());
}
}// namespace fusion
}// namespace adsk

#undef ADSK_FUSION_AUTOCONSTRAININPUT_API